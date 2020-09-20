from pyexcel_io.constants import KEYWORD_TSV_DIALECT
from pyexcel_io.writers.csv_memory_writer import CsvMemoryWriter


class TsvMemoryWriter(CsvMemoryWriter):
    def open(self, file_alike_object, **keywords):
        super().open(
            file_alike_object, dialect=KEYWORD_TSV_DIALECT, **keywords
        )
