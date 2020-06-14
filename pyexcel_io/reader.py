from pyexcel_io.plugins import NEW_READERS
from pyexcel_io._compact import OrderedDict


class Reader(object):
    def __init__(self, file_type, library=None):
        self.file_type = file_type
        self.library = library

    def open(self, file_name, **keywords):
        self.reader = NEW_READERS.get_a_plugin(
            self.file_type, location="file", library=self.library
        )
        return self.reader.open(file_name, **keywords)

    def open_content(self, file_content, **keywords):
        self.reader = NEW_READERS.get_a_plugin(
            self.file_type, location="content", library=self.library
        )
        return self.reader.open(file_content, **keywords)

    def open_stream(self, file_stream, **keywords):
        self.reader = NEW_READERS.get_a_plugin(
            self.file_type, location="memory", library=self.library
        )
        return self.reader.open(file_stream, **keywords)

    def read_sheet_by_name(self, sheet_name):
        """
        read a named sheet from a excel data book
        """
        for index, content in enumerate(self.reader.content_array):
            if content.name == sheet_name:
                return self.reader.read_sheet(index)
        else:
            raise ValueError("Cannot find sheet %s" % sheet_name)

    def read_sheet_by_index(self, sheet_index):
        """
        read an indexed sheet from a excel data book
        """
        try:
            return self.reader.read_sheet(sheet_index)

        except IndexError:
            self.close()
            raise

    def read_all(self):
        """
        read everything from a excel data book
        """
        result = OrderedDict()
        for index, sheet in enumerate(self.reader.content_array):
            result.update(self.reader.read_sheet(index))
        return result

    def read_many(self, sheets):
        """
        read everything from a excel data book
        """
        result = OrderedDict()
        for sheet in sheets:
            if isinstance(sheet, int):
                result.update(self.read_sheet_by_index(sheet))
            else:
                result.update(self.read_sheet_by_name(sheet))
        return result

    def close(self):
        return self.reader.close()

    def __enter__(self):
        return self

    def __exit__(self, a_type, value, traceback):
        self.close()
