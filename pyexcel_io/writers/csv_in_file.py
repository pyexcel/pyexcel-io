from pyexcel_io import constants
from pyexcel_io.writers.csv_sheet import CSVFileWriter
from pyexcel_io.plugin_api.abstract_writer import IWriter


class CsvFileWriter(IWriter):
    def __init__(self, file_alike_object, file_type, **keywords):
        self._file_alike_object = file_alike_object
        self._keywords = keywords
        if file_type == constants.FILE_FORMAT_TSV:
            self._keywords["dialect"] = constants.KEYWORD_TSV_DIALECT
        self.__index = 0
        self.writer = None

    def create_sheet(self, name):
        self.writer = CSVFileWriter(
            self._file_alike_object,
            name,
            sheet_index=self.__index,
            **self._keywords
        )
        self.__index = self.__index + 1
        return self.writer

    def close(self):
        if self.writer:
            self.writer.close()
