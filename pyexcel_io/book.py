"""
    pyexcel_io.base
    ~~~~~~~~~~~~~~~~~~~

    The io interface to file extensions

    :copyright: (c) 2014-2016 by Onni Software Ltd.
    :license: New BSD License, see LICENSE for more details
"""
from abc import abstractmethod

from .manager import RWManager
from ._compact import PY2, OrderedDict, isstream, StringIO
from .constants import (
    MESSAGE_ERROR_03,
    MESSAGE_WRONG_IO_INSTANCE
)


class RWInterface(object):
    """
    The common methods for book reader and writer
    """
    def RWInterface(self):
        self.file_type = None
        
    def open(self, file_name, **keywords):
        pass

    def open_stream(self, file_stream, **keywords):
        pass

    def set_type(self, file_type):
        self.file_type = file_type

    def close(self):
        pass



class BookReader(RWInterface):
    """
    Standard book reader
    """
    def __init__(self):
        self.reader = None
        self.file_name = None
        self.file_stream = None
        self.keywords = None

    def open(self, file_name, **keywords):
        self.file_name = file_name
        self.keywords = keywords

    def open_stream(self, file_stream, **keywords):
        if RWManager.validate_io(self.file_type, file_stream):
            self.file_stream = file_stream
            self.keywords = keywords
        else:
            raise IOError(MESSAGE_WRONG_IO_INSTANCE)

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
        named_contents = list(filter(lambda nc: nc.name == sheet_name,
                                     self.native_book))
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


class BookWriter(RWInterface):
    """
    Standard book writer
    """
    def __init__(self):
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

    def write(self, incoming_dict):
        for sheet_name in incoming_dict:
            sheet_writer = self.create_sheet(sheet_name)
            if sheet_writer:
                sheet_writer.write_array(incoming_dict[sheet_name])
                sheet_writer.close()

    @abstractmethod
    def create_sheet(self, sheet_name):
        pass
