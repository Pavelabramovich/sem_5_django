import pathlib

from django.db.models import FileField


class NamedFileField(FileField):
    def __init__(
        self,
        *args,
        get_filename=None,
        **kwargs
    ):
        super().__init__(*args, **kwargs)

        if get_filename is None:
            self.get_filename = lambda file: file.name
        else:
            self.get_filename = lambda file: f"{get_filename(file.instance)}{(extension := pathlib.Path(file.name).suffix)}"

    def pre_save(self, model_instance, add):
        file = super(FileField, self).pre_save(model_instance, add)

        if file and not file._committed:
            filename = self.get_filename(file)
            file.save(filename, file.file, save=False)

        return file


