from ._compact import OrderedDict, StringIO, BytesIO, isstream, PY2
from abc import abstractmethod
from .base import NamedContent
from .constants import (
    DEFAULT_SEPARATOR,
    DEFAULT_SHEET_NAME,
    MESSAGE_ERROR_03,
    MESSAGE_WRONG_IO_INSTANCE,
    FILE_FORMAT_CSV,
    FILE_FORMAT_TSV,
    FILE_FORMAT_CSVZ,
    FILE_FORMAT_TSVZ,
    FILE_FORMAT_ODS,
    FILE_FORMAT_XLS,
    FILE_FORMAT_XLSX,
    FILE_FORMAT_XLSM,
    KEYWORD_TSV_DIALECT,
    DB_SQL,
    DB_DJANGO
)


# Please also register here
TEXT_STREAM_TYPES = [FILE_FORMAT_CSV, FILE_FORMAT_TSV]

# Please also register here
BINARY_STREAM_TYPES = [FILE_FORMAT_CSVZ, FILE_FORMAT_TSVZ,
                       FILE_FORMAT_ODS, FILE_FORMAT_XLS,
                       FILE_FORMAT_XLSX, FILE_FORMAT_XLSM]


def get_io(file_type):
    """A utility function to help you generate a correct io stream

    :param file_type: a supported file type
    :returns: a appropriate io stream, None otherwise
    """
    if file_type in TEXT_STREAM_TYPES:
        return StringIO()
    elif file_type in BINARY_STREAM_TYPES:
        return BytesIO()
    else:
        return None

def validate_io(file_type, io):
    if file_type in TEXT_STREAM_TYPES:
        return isinstance(io, StringIO)
    elif file_type in BINARY_STREAM_TYPES:
        return isinstance(io, BytesIO)
    else:
        return False


class Reader(object):
    def __init__(self, file_type, reader_class):
        self.reader_class = reader_class
        self.file_type = file_type
        self.reader = None
        self.file_name = None
        self.file_stream = None
        self.keywords = None

    def open(self, file_name, **keywords):
        self.file_name = file_name
        self.keywords = keywords

    def open_stream(self, file_stream, **keywords):
        if validate_io(self.file_type, file_stream):
            self.file_stream = file_stream
            self.keywords = keywords
        else:
            raise IOError(MESSAGE_WRONG_IO_INSTANCE)

    def open_content(self, file_content, **keywords):
        io = get_io(self.file_type)
        if not PY2:
            if (isinstance(io, StringIO) and isinstance(file_content, bytes)):
                content = file_content.decode('utf-8')
            else:
                content = file_content
            io.write(content)
        else:
            io.write(file_content)
        io.seek(0)
        self.open_stream(io, **keywords)

    def read_sheet_by_name(self, sheet_name):
        return self._read_with_parameters(load_sheet_with_name=sheet_name)

    def read_sheet_by_index(self, sheet_index):
        return self._read_with_parameters(load_sheet_at_index=sheet_index)

    def read_all(self):
        return self._read_with_parameters()

    def _read_with_parameters(self, load_sheet_with_name=None, load_sheet_at_index=None):
        if self.file_name:
            if self.file_name in [DB_SQL, DB_DJANGO]:
                reader = self.reader_class(**self.keywords)
            else:
                reader = self.reader_class(
                    self.file_name,
                    load_sheet_with_name=load_sheet_with_name,
                    load_sheet_at_index=load_sheet_at_index,
                    **self.keywords)
        else:
            reader = self.reader_class(None,
                                       file_content=self.file_stream,
                                       load_sheet_with_name=load_sheet_with_name,
                                       load_sheet_at_index=load_sheet_at_index,
                                       **self.keywords)
        return reader.sheets()


class NewBookReader(Reader):
    """
    Standard reader
    """
    def __init__(self, file_type):
        Reader.__init__(self, file_type, None)

    def open(self, file_name, **keywords):
        Reader.open(self, file_name, **keywords)
        self.native_book = self.load_from_file(file_name)

    def open_stream(self, file_stream, **keywords):
        Reader.open_stream(self, file_stream, **keywords)
        self.native_book = self.load_from_stream(file_stream)

    def read_sheet_by_name(self, sheet_name):
        named_contents  = list(filter(lambda nc: nc.name == sheet_name, self.native_book))
        if len(named_contents) == 1:
            return {named_contents[0].name: self.read_sheet(named_contents[0])}
        else:
            self.close()
            raise ValueError("Cannot find sheet %s" % sheet_name)

    def read_sheet_by_index(self, sheet_index):
        try:
            sheet = self.native_book[sheet_index]
            return {sheet.name: self.read_sheet(sheet)}
        except IndexError:
            self.close()
            raise

    def read_all(self):
        result = OrderedDict()
        for sheet in self.native_book:
            result[sheet.name] = self.read_sheet(sheet)
        return result
    

    @abstractmethod
    def read_sheet(self, native_sheet):
        """Return a context specific sheet from a native sheet
        """
        pass

    @abstractmethod
    def load_from_memory(self, file_content):
        """Load content from memory

        :params stream file_content: the actual file content in memory
        :returns: a book
        """
        pass

    @abstractmethod
    def load_from_file(self, file_name):
        """Load content from a file

        :params str filename: an accessible file path
        :returns: a book
        """
        pass

    def close(self):
        pass


class Writer(object):
    def __init__(self, file_type, writer_class):
        self.file_type = file_type
        self.writer_class = writer_class
        self.writer = None
        self.file_alike_object = None

    def open_content(self, file_content, **keywords):
        pass

    def open(self, file_name, **keywords):
        self.file_alike_object = file_name
        self.keywords = keywords

    def open_stream(self, file_stream, **keywords):
        if isstream(file_stream):
            if not validate_io(self.file_type, file_stream):
                raise IOError(MESSAGE_WRONG_IO_INSTANCE)
        else:
            raise IOError(MESSAGE_ERROR_03)
        self.open(file_stream, **keywords)

    def write(self, data):
        self.writer = self.writer_class(self.file_alike_object,
                                        **self.keywords)
        self.writer.write(data)

    def close(self):
        if self.writer:
            self.writer.close()


class NewWriter(Writer):
    def __init__(self, file_type):
        Writer.__init__(self, file_type, None)

    def open(self, file_name, **keywords):
        Writer.open(self, file_name, **keywords)

    def write(self, incoming_dict):
        for sheet_name in incoming_dict:
            sheet_writer = self.create_sheet(sheet_name)
            if sheet_writer:
                sheet_writer.write_array(incoming_dict[sheet_name])
                sheet_writer.close()

    def close(self):
        pass


