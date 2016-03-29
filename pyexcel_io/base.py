"""
    pyexcel_io.base
    ~~~~~~~~~~~~~~~~~~~

    The io interface to file extensions

    :copyright: (c) 2014-2016 by Onni Software Ltd.
    :license: New BSD License, see LICENSE for more details
"""
from abc import ABCMeta, abstractmethod

from ._compact import PY2, is_generator, OrderedDict, isstream
from ._compact import StringIO, BytesIO
from .utils import resolve_missing_readers, resolve_missing_writers
from .constants import (
    DEFAULT_SHEET_NAME,
    MESSAGE_ERROR_03,
    MESSAGE_WRONG_IO_INSTANCE,
    MESSAGE_LOADING_FORMATTER,
    DB_SQL,
    DB_DJANGO
)


class NamedContent:
    """
    Helper class for content that does not have a name
    """

    def __init__(self, name, payload):
        self.name = name
        self.payload = payload


def add_metaclass(metaclass):
    """
    Class decorator for creating a class with a metaclass.
    """
    def wrapper(cls):
        orig_vars = cls.__dict__.copy()
        slots = orig_vars.get('__slots__')
        if slots is not None:
            if isinstance(slots, str):
                slots = [slots]
            for slots_var in slots:
                orig_vars.pop(slots_var)
        orig_vars.pop('__dict__', None)
        orig_vars.pop('__weakref__', None)
        return metaclass(cls.__name__, cls.__bases__, orig_vars)
    return wrapper


@add_metaclass(ABCMeta)
class SheetReader(object):
    """
    Generic sheet reader
    """
    def __init__(self, sheet, **keywords):
        self.native_sheet = sheet
        self.keywords = keywords

    @abstractmethod
    def to_array(self):
        """2 dimentional repsentation of the content
        """
        pass


@add_metaclass(ABCMeta)
class SheetWriter(object):
    """
    Generic sheet writer
    """

    def __init__(self, native_book, native_sheet, name, **keywords):
        if name:
            sheet_name = name
        else:
            sheet_name = DEFAULT_SHEET_NAME
        self.native_book = native_book
        self.native_sheet = native_sheet
        self.keywords = keywords
        self.set_sheet_name(sheet_name)

    def set_sheet_name(self, name):
        """
        Set sheet name
        """
        pass

    def set_size(self, size):
        """
        size of the content will be given
        """
        pass

    @abstractmethod
    def write_row(self, array):
        """
        write a row into the file
        """
        pass

    def write_array(self, table):
        """
        For standalone usage, write an array
        """
        if not is_generator(table):
            rows = len(table)
            if rows < 1:
                return
            columns = max([len(row) for row in table])
            self.set_size((rows, columns))
        for row in table:
            self.write_row(row)

    def close(self):
        """
        This call actually save the file
        """
        pass


class BookReader(object):
    """
    Standard reader
    """
    def __init__(self, file_type):
        self.file_type = file_type
        self.reader = None
        self.file_name = None
        self.file_stream = None
        self.keywords = None

    def open(self, file_name, **keywords):
        self.file_name = file_name
        self.keywords = keywords
        self.native_book = self.load_from_file(file_name)

    def open_stream(self, file_stream, **keywords):
        if RWManager.validate_io(self.file_type, file_stream):
            self.file_stream = file_stream
            self.keywords = keywords
        else:
            raise IOError(MESSAGE_WRONG_IO_INSTANCE)
        self.native_book = self.load_from_stream(file_stream)

    def open_content(self, file_content, **keywords):
        io = RWManager.get_io(self.file_type)
        if PY2:
            io.write(file_content)
        else:
            if (isinstance(io, StringIO) and isinstance(file_content, bytes)):
                content = file_content.decode('utf-8')
            else:
                content = file_content
            io.write(content)
        io.seek(0)
        self.open_stream(io, **keywords)

    def read_sheet_by_name(self, sheet_name):
        named_contents = list(filter(lambda nc: nc.name == sheet_name, self.native_book))
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
    def load_from_stream(self, file_content):
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


class BookWriter(object):
    def __init__(self, file_type):
        self.file_type = file_type
        self.writer = None
        self.file_alike_object = None

    def open(self, file_name, **keywords):
        self.file_alike_object = file_name
        self.keywords = keywords

    def open_stream(self, file_stream, **keywords):
        if isstream(file_stream):
            if not RWManager.validate_io(self.file_type, file_stream):
                raise IOError(MESSAGE_WRONG_IO_INSTANCE)
        else:
            raise IOError(MESSAGE_ERROR_03)
        self.open(file_stream, **keywords)

    def open_content(self, file_content, **keywords):
        pass

    def write(self, incoming_dict):
        for sheet_name in incoming_dict:
            sheet_writer = self.create_sheet(sheet_name)
            if sheet_writer:
                sheet_writer.write_array(incoming_dict[sheet_name])
                sheet_writer.close()

    @abstractmethod
    def create_sheet(self, sheet_name):
        pass

    def close(self):
        pass


class RWManager(object):
    reader_factories = {}
    writer_factories = {}
    text_stream_types = []
    binary_stream_types = []

    @staticmethod
    def register_file_type_as_text_stream(file_type):
        RWManager.text_stream_types.append(file_type)

    @staticmethod
    def register_file_type_as_binary_stream(file_type):
        RWManager.binary_stream_types.append(file_type)


    @staticmethod
    def register_readers(file_type_reader_dict):
        for file_type, reader_class in file_type_reader_dict.items():
            RWManager.register_a_reader(file_type, reader_class)

    @staticmethod
    def register_a_reader(file_type, reader_class):
        RWManager._add_a_handler(RWManager.reader_factories,
                                 file_type, reader_class)

    @staticmethod
    def register_writers(file_type_writer_dict):
        for file_type, writer_class in file_type_writer_dict.items():
            RWManager.register_a_writer(file_type, writer_class)

    @staticmethod
    def register_a_writer(file_type, writer_class):
        RWManager._add_a_handler(RWManager.writer_factories,
                                 file_type, writer_class)

    @staticmethod
    def _add_a_handler(factories, file_type, handler):
        if file_type in factories:
            print("Warning! %s has been registered" % file_type)
        factories[file_type] = handler

    @staticmethod
    def create_reader(file_type):
        if file_type in RWManager.reader_factories:
            reader_class = RWManager.reader_factories[file_type]
            return reader_class()
        else:
            resolve_missing_readers(file_type)

    @staticmethod
    def create_writer(file_type):
        if file_type in RWManager.writer_factories:
            writer_class = RWManager.writer_factories[file_type]
            return writer_class()
        else:
            resolve_missing_writers(file_type)


    @staticmethod
    def get_io(file_type):
        """A utility function to help you generate a correct io stream
    
        :param file_type: a supported file type
        :returns: a appropriate io stream, None otherwise
        """
        if file_type in RWManager.text_stream_types:
            return StringIO()
        elif file_type in RWManager.binary_stream_types:
            return BytesIO()
        else:
            return None
    
    
    @staticmethod
    def validate_io(file_type, stream):
        if file_type in RWManager.text_stream_types:
            return isinstance(stream, StringIO)
        elif file_type in RWManager.binary_stream_types:
            return isinstance(stream, BytesIO)
        else:
            return False
