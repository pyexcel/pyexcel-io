from pyexcel_io.constants import FILE_FORMAT_TSVZ, KEYWORD_TSV_DIALECT
from pyexcel_io.writers.csvz_writer import CsvZipWriter


class TsvZipWriter(CsvZipWriter):
    def __init__(self):
        super().__init__()
        self._file_type = FILE_FORMAT_TSVZ

    def open(self, file_name, **keywords):
        super().open(file_name, dialect=KEYWORD_TSV_DIALECT, **keywords)
