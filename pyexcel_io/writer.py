from pyexcel_io.plugins import NEW_WRITERS


class Writer(object):
    def __init__(self, file_type, library=None):
        self.file_type = file_type
        self.library = library
        self.keyboards = None

    def open(self, file_name, **keywords):
        writer_class = NEW_WRITERS.get_a_plugin(
            self.file_type, library=self.library, location="file"
        )
        self.writer = writer_class(file_name, self.file_type, **keywords)

    def open_content(self, file_stream, **keywords):
        # if not isstream(file_stream):
        #    raise IOError(MESSAGE_ERROR_03)
        writer_class = NEW_WRITERS.get_a_plugin(
            self.file_type, library=self.library, location="content"
        )
        self.writer = writer_class(file_stream, self.file_type, **keywords)

    def open_stream(self, file_stream, **keywords):
        writer_class = NEW_WRITERS.get_a_plugin(
            self.file_type, library=self.library, location="memory"
        )
        self.writer = writer_class(file_stream, self.file_type, **keywords)

    def write(self, incoming_dict):
        self.writer.write(incoming_dict)

    def close(self):
        self.writer.close()

    def __enter__(self):
        return self

    def __exit__(self, a_type, value, traceback):
        self.close()
