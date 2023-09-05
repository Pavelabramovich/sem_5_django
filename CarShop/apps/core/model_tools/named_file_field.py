import pathlib

from django.db.models import FileField


class NamedFileField(FileField):
    def __init__(
        self,
        *args,
        get_filename,
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.get_filename = get_filename

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        kwargs["get_filename"] = self.get_filename
        return name, path, args, kwargs

    def pre_save(self, model_instance, add):
        file = super(FileField, self).pre_save(model_instance, add)

        if file and not file._committed:
            filename = f"{self.get_filename(file.instance)}{(extension := pathlib.Path(file.name).suffix)}"
            file.save(filename, file.file, save=False)

        return file


