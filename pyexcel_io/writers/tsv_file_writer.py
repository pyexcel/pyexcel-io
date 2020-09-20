from pyexcel_io.writers.csv_file_writer import CsvFileWriter


class TsvFileWriter(CsvFileWriter):
    def open(self, file_alike_object, **keywords):
        super(TsvFileWriter).open(file_alike_object, dialect="tsv", **keywords)
