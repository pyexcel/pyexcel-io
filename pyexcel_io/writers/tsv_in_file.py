from pyexcel_io.constants import KEYWORD_TSV_DIALECT
from pyexcel_io.writers.csv_in_file import CsvFileWriter


class TsvFileWriter(CsvFileWriter):
    def __init__(self, file_alike_object, **keywords):
        super().__init__(
            file_alike_object, dialect=KEYWORD_TSV_DIALECT, **keywords
        )
