from pyexcel_io.plugins import NEW_WRITERS
from pyexcel_io._compact import isstream

from .constants import MESSAGE_ERROR_03


class Writer(object):
    def __init__(self, file_type, library=None):
        self.file_type = file_type
        self.library = library
        self.keyboards = None

    def open(self, file_name, **keywords):
        self.writer = NEW_WRITERS.get_a_plugin(
            self.file_type, library=self.library, location="file"
        )
        self.writer.open(file_name, **keywords)

    def open_content(self, file_stream, **keywords):
        if not isstream(file_stream):
            raise IOError(MESSAGE_ERROR_03)
        self.writer = NEW_WRITERS.get_a_plugin(
            self.file_type, library=self.library, location="content"
        )
        self.writer.open(file_stream, **keywords)

    def open_stream(self, file_stream, **keywords):
        self.writer = NEW_WRITERS.get_a_plugin(
            self.file_type, library=self.library, location="memory"
        )
        self.writer.open(file_stream, **keywords)

    def write(self, incoming_dict):
        for sheet_name in incoming_dict:
            sheet_writer = self.writer.create_sheet(sheet_name)
            if sheet_writer:
                sheet_writer.write_array(incoming_dict[sheet_name])
                sheet_writer.close()
            else:
                raise Exception("Cannot create a sheet writer!")

    def close(self):
        self.writer.close()

    def __enter__(self):
        return self

    def __exit__(self, a_type, value, traceback):
        self.close()
