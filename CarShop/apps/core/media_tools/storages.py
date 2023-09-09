import os
from pathlib import Path
from datetime import datetime

from django.core.files.storage import FileSystemStorage


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

        if coded_names:
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
