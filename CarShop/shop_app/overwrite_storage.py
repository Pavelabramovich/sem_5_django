import os
from pathlib import Path
import random
from django.core.files import File
from io import BytesIO
from PIL import Image

from django.core.files.storage import FileSystemStorage
from datetime import datetime

from django.db.models import ImageField
from django.db.models.fields.files import ImageFieldFile
from imagekit.cachefiles.backends import CacheFileState

from .first_or_default import first_or_default
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
            location=None,
            base_url=None,
            file_permissions_mode=None,
            directory_permissions_mode=None,
            get_code=lambda name, content: datetime.now().strftime("%d-%m-%Y-%H-%M-%S-%f")
    ):
        self.get_code = get_code
        super().__init__(
            location=location,
            base_url=base_url,
            file_permissions_mode=file_permissions_mode,
            directory_permissions_mode=directory_permissions_mode
        )

    def exists(self, name):
        with_code = bool(self.__get_coded_filenames(name))
        without_code = super().exists(name)

        return with_code or without_code

    def __get_coded_filenames(self, name, default=None):
        splitted_name = name.split(os.extsep)
        only_name = '.'.join(splitted_name[:-1])
        extension = splitted_name[-1]

        file_matches = [str(path) for path in Path(self.location).glob(f'{only_name}*')]
     #   print(name)
     #   print(splitted_name)
     #   print(file_matches)
        file_codes = [path.split(os.extsep)[-2] for path in file_matches]

        return [f"{only_name}.{file_code}.{extension}" for file_code in file_codes]

    def _open(self, name, mode="rb"):
        if coded_names := self.__get_coded_filenames(name):
            name = coded_names[0]

        return super()._open(name, mode)

    def delete(self, name):
        if coded_names := self.__get_coded_filenames(name):
            for coded_name in coded_names:
                super().delete(coded_name)
        else:
            super().delete(name)

    def _save(self, name, content):

        splitted_name = name.split(os.extsep)

        only_name = splitted_name[:-1]
        extension = splitted_name[-1]

        code = self.get_code(name, content)

        return super()._save(f"{'.'.join(only_name)}.{code}.{extension}", content)


class AvatarStorage(OverwriteStorage, CodedStorage):
    def __init__(
            self,
            location=None,
            base_url=None,
            file_permissions_mode=None,
            directory_permissions_mode=None,
            avatar_size=300
    ):
        self.avatar_size = avatar_size
        super().__init__(
            location=location,
            base_url=base_url,
            file_permissions_mode=file_permissions_mode,
            directory_permissions_mode=directory_permissions_mode
        )


class AvatarFieldFile(ImageFieldFile):
    def __get_avatar_file(self, content):
        AVATAR_SIZE = 300
        print(self.instance.pk)

        if content:
            with Image.open(content) as image:
                square_avatar = image.copy()
        else:
            random.seed(self.instance.pk)
            avatar_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            avatar_background = create_background((AVATAR_SIZE, AVATAR_SIZE), avatar_color)

            default_avatar_path = self.storage.path(self.field.default)
            default_avatar = Image.open(default_avatar_path).convert('RGBA')

            square_avatar = Image.alpha_composite(avatar_background, default_avatar)

        new_avatar = crop_to_circle(square_avatar, AVATAR_SIZE)

        blob = BytesIO()
        new_avatar.save(blob, 'PNG')

        return File(blob)

    def save(self, name, content, save=True):
        print(name)
        print("save")
        print(f"o{content}o")
        print(bool(content))

        content = self.__get_avatar_file(content)

        name = self.field.generate_filename(self.instance, f"avatar_{self.instance.pk}.png")
        self.name = self.storage.save(name, content, max_length=self.field.max_length)
        setattr(self.instance, self.field.attname, self.name)
        self._committed = True

        # Save the object because it has changed, unless save is False
        if save:
            self.instance.save()

    def _get_file(self):
        if not self:
            self._file = self.__get_avatar_file(None)

        if getattr(self, "_file", None) is None:
            self._file = self.storage.open(self.name, "rb")
        return self._file





class AvatarField(ImageField):
    attr_class = AvatarFieldFile


# if self.avatar and self.avatar.name != self.avatar.field.default:
#     with Image.open(self.avatar.path) as image:
#         square_avatar = image.copy()
#
#     os.remove(self.avatar.path)
# else:
#     random.seed(user_id)
#     avatar_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
#     avatar_background = create_background((self.AVATAR_SIZE, self.AVATAR_SIZE), avatar_color)
#
#     default_avatar_path = self.avatar.storage.path(self.avatar.field.default)
#     default_avatar = Image.open(default_avatar_path).convert('RGBA')
#
#     square_avatar = Image.alpha_composite(avatar_background, default_avatar)
#
# new_avatar = crop_to_circle(square_avatar, self.AVATAR_SIZE)
#
# blob = BytesIO()
# new_avatar.save(blob, 'PNG')
#
# self.avatar.save(f"avatar_{user_id}.png", File(blob), save=False)
#
# super().save(*args, **kwargs)

