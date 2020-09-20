from pyexcel_io.constants import KEYWORD_TSV_DIALECT
from pyexcel_io.writers.csv_file_writer import CsvFileWriter


class TsvFileWriter(CsvFileWriter):
    def open(self, file_alike_object, **keywords):
        super().open(
            file_alike_object, dialect=KEYWORD_TSV_DIALECT, **keywords
        )
