from pyexcel_io.constants import FILE_FORMAT_TSVZ, KEYWORD_TSV_DIALECT
from pyexcel_io.writers.csvz_writer import CsvZipWriter


class TsvZipWriter(CsvZipWriter):
    def __init__(self, file_name, **keywords):
        super().__init__(file_name, dialect=KEYWORD_TSV_DIALECT, **keywords)
        self._file_type = FILE_FORMAT_TSVZ
