from pyexcel_io.writers.csv_memory_writer import CsvMemoryWriter


class TsvMemoryWriter(CsvMemoryWriter):
    def open(self, file_alike_object, **keywords):
        super(TsvMemoryWriter).open(
            file_alike_object, dialect="tsv", **keywords
        )
