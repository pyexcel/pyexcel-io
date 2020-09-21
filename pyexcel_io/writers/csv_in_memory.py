from pyexcel_io.writers.csv_sheet import CSVMemoryWriter


class CsvMemoryWriter:
    def __init__(self):
        self.__index = 0

    def open(self, file_alike_object, **keywords):
        self._file_alike_object = file_alike_object
        self._keywords = keywords

    def create_sheet(self, name):
        writer_class = CSVMemoryWriter
        writer = writer_class(
            self._file_alike_object,
            name,
            sheet_index=self.__index,
            **self._keywords
        )
        self.__index = self.__index + 1
        return writer

    def close(self):
        pass
