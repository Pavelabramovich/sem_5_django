from apps.core.model_tools import NamedFileField
from django.db.models import ImageField


class NamedImageField(NamedFileField, ImageField):
    def __init__(
        self,
        width_field=None,
        height_field=None,
        get_filename=lambda obj: "123",
        **kwargs,
    ):
        self.width_field, self.height_field = width_field, height_field
        super().__init__(get_filename=get_filename, **kwargs)
