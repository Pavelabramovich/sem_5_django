from io import BytesIO

from django.core.files import File
from django.db.models import ImageField
from django.db.models.fields.files import ImageFieldFile, FileField
from PIL import Image

from apps.core.image_tools import create_background, crop_to_circle
from apps.core.media_tools import OverwriteCodedStorage


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
        if image and image.name != self.default:
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
        image = super(FileField, self).pre_save(model_instance, add)

        if not image or not getattr(image, '_commited', False):
            filename = f"{self.get_filename(image.instance)}.png"
            avatar_file = self.__get_avatar_file(image)
            image.save(filename, avatar_file, save=False)

        return image


