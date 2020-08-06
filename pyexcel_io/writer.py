from pyexcel_io.plugins import NEW_WRITERS


class Writer(object):
    def __init__(self, file_type, library):
        self.file_type = file_type
        self.library = library
        self.keyboards = None

    def open(self, file_name, **keywords):
        self.writer = NEW_WRITERS.get_a_plugin(
            self.file_type, library=self.library, location="file"
        )
        self.writer.open(file_name, **keywords)

    def open_content(self, file_stream, **keywords):
        self.writer = NEW_WRITERS.get_a_plugin(
            self.file_type, library=self.library, location="content"
        )
        self.writer.open_content(file_stream, **keywords)

    def open_stream(self, file_stream, **keywords):
        self.writer = NEW_WRITERS.get_a_plugin(
            self.file_type, library=self.library, location="memory"
        )
        self.writer.open_stream(file_stream, **keywords)

    def write(self, incoming_dict):
        self.writer.write(incoming_dict)

    def create_sheet(self, sheet_name):
        return self.writer.create_sheet(sheet_name)

    def close(self):
        self.writer.close()

    def __enter__(self):
        return self

    def __exit__(self, a_type, value, traceback):
        self.close()
