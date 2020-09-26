from pyexcel_io.writers.csv_sheet import CSVMemoryWriter


class CsvMemoryWriter:
    def __init__(self, file_alike_object, **keywords):
        self._file_alike_object = file_alike_object
        self._keywords = keywords
        self.__index = 0

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

    def write(self, incoming_dict):
        for sheet_name in incoming_dict:
            sheet_writer = self.create_sheet(sheet_name)
            if sheet_writer:
                sheet_writer.write_array(incoming_dict[sheet_name])
                sheet_writer.close()
            else:
                raise Exception("Cannot create a sheet writer!")

    def close(self):
        pass
