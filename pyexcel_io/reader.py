from pyexcel_io.plugins import READERS


class Reader(object):
    def __init__(self, file_type, library=None):
        self.reader = READERS.get_a_plugin(file_type, library)

    def open(self, file_name, **keywords):
        return self.reader.open(file_name, **keywords)

    def open_content(self, file_content, **keywords):
        return self.reader.open_content(file_content, **keywords)

    def open_stream(self, file_stream, **keywords):
        return self.reader.open_stream(file_stream, **keywords)

    def read_sheet_by_index(self, sheet_index):
        return self.reader.read_sheet_by_index(sheet_index)

    def read_sheet_by_name(self, sheet_name):
        return self.reader.read_sheet_by_name(sheet_name)

    def read_many(self, sheets):
        return self.reader.read_many(sheets)

    def read_all(self):
        return self.reader.read_all()

    def close(self):
        return self.reader.close()

    def __enter__(self):
        return self

    def __exit__(self, a_type, value, traceback):
        self.close()
