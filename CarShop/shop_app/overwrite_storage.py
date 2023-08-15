import os
from pathlib import Path
import random
from django.core.files import File
from io import BytesIO
from PIL import Image

from django.core.files.storage import FileSystemStorage
from datetime import datetime

from django.db.models import ImageField
from django.db.models.fields.files import ImageFieldFile, FileField
from .img_tools import create_background, crop_to_circle


class OverwriteStorage(FileSystemStorage):
    def _save(self, name, content):
        if self.exists(name):
            self.delete(name)

        return super()._save(name, content)

    def get_available_name(self, name, max_length=None):
        return name


class CodedStorage(FileSystemStorage):
    def __init__(
        self,
        get_code=lambda name, content: datetime.now().strftime("%d-%m-%Y-%H-%M-%S-%f"),
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.get_code = get_code

    def exists(self, name):
        return bool(self.__get_matched_filenames(name))

    def __get_matched_filenames(self, name):
        if super().exists(name):
            return [name]

        else:
            splitted_name = name.split(os.extsep)

            *only_name, extension = splitted_name
            only_name = os.extsep.join(only_name)

            file_matches = [str(path) for path in Path(self.location).glob(f'{only_name}*')]
            file_codes = [path.split(os.extsep)[-2] for path in file_matches]

            return [f"{only_name}{os.extsep}{file_code}{os.extsep}{extension}" for file_code in file_codes]

    def _open(self, name, mode="rb"):
        coded_names = self.__get_matched_filenames(name)
        name = coded_names[0]

        return super()._open(name, mode)

    def delete(self, name):
        coded_names = self.__get_matched_filenames(name)
        for coded_name in coded_names:
            super().delete(coded_name)

    def _save(self, name, content):
        splitted_name = name.split(os.extsep)

        *only_name, extension = splitted_name
        only_name = os.extsep.join(only_name)

        code = self.get_code(name, content)

        return super()._save(f"{only_name}{os.extsep}{code}{os.extsep}{extension}", content)


class OverwriteCodedStorage(OverwriteStorage, CodedStorage):
    def __init__(self, **kwargs):
        super(OverwriteStorage, self).__init__(**kwargs)


class AvatarFieldFile(ImageFieldFile):
    def _require_file(self):
        if not self:
            self.file = None


class AvatarField(ImageField):
    attr_class = AvatarFieldFile

    def __init__(
        self,
        avatar_size=300,
        get_filename=lambda instance: "avatar",
        get_color=lambda instance: (240, 29, 0), # Red
        storage=OverwriteCodedStorage(),
        **kwargs
    ):
        super().__init__(**kwargs)
        self.avatar_size = avatar_size
        self.get_filename = get_filename
        self.get_color = get_color
        self.storage = storage

    def __get_avatar_file(self, image):
        if image:
            with Image.open(image.file) as row_image:
                row_avatar = row_image.copy()
        else:
            avatar_color = self.get_color(image.instance)
            avatar_background = create_background((self.avatar_size, self.avatar_size), avatar_color)

            default_avatar_path = self.storage.path(self.default)
            default_avatar = Image.open(default_avatar_path).convert('RGBA')

            row_avatar = Image.alpha_composite(avatar_background, default_avatar)

        circle_avatar = crop_to_circle(row_avatar, self.avatar_size)

        blob = BytesIO()
        circle_avatar.save(blob, 'PNG')

        return File(blob)

    def pre_save(self, model_instance, add):
        print("-----pre_save------")
        print(f"{model_instance.pk=}")

        image = super(FileField, self).pre_save(model_instance, add)

        if not image or not getattr(image, '_commited', False):
            filename = f"{self.get_filename(image.instance)}.png"
            avatar_file = self.__get_avatar_file(image)
            image.save(filename, avatar_file, save=False)

        return image


