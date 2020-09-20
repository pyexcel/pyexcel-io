import zipfile

from pyexcel_io.constants import FILE_FORMAT_CSVZ, DEFAULT_SHEET_NAME

from .csvz import CSVZipSheetWriter


class CsvZipWriter(object):
    """
    csvz writer

    It is better to store csv files as a csvz as it saves your disk space.
    Pyexcel-io had the facility to unzip it for you or you could use
    any other unzip software.
    """

    def __init__(self):
        self.zipfile = None
        self._keywords = None
        self._file_type = FILE_FORMAT_CSVZ

    def open(self, file_name, **keywords):
        self.zipfile = zipfile.ZipFile(file_name, "w", zipfile.ZIP_DEFLATED)
        self._keywords = keywords

    def create_sheet(self, name):
        given_name = name
        if given_name is None:
            given_name = DEFAULT_SHEET_NAME
        writer = CSVZipSheetWriter(
            self.zipfile, given_name, self._file_type[:3], **self._keywords
        )
        return writer

    def close(self):
        if self.zipfile:
            self.zipfile.close()

    def set_type(self, _):
        pass
