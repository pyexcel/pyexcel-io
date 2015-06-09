"""
    pyexcel_io.base
    ~~~~~~~~~~~~~~~~~~~

    The io interface to file extensions

    :copyright: (c) 2014-2015 by Onni Software Ltd.
    :license: New BSD License, see LICENSE for more details
"""
import sys
import datetime
from abc import ABCMeta, abstractmethod, abstractproperty
if sys.version_info[0] == 2 and sys.version_info[1] < 7:
    from ordereddict import OrderedDict
else:
    from collections import OrderedDict
from .constants import DEFAULT_SHEET_NAME


def add_metaclass(metaclass):
    """Class decorator for creating a class with a metaclass."""
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


class NamedContent:
    """Helper class for content that does not have a name"""
    def __init__(self, name, payload):
        self.name = name
        self.payload = payload


@add_metaclass(ABCMeta)
class SheetReaderBase(object):
    """
    sheet
    """
    def __init__(self, sheet, **keywords):
        self.native_sheet = sheet
        self.keywords = keywords

    @abstractproperty
    def name(self):
        pass

    @abstractmethod
    def to_array(self):
        """2 dimentional repsentation of the content
        """
        pass


class SheetReader(SheetReaderBase):

    @abstractmethod
    def number_of_rows(self):
        """
        Number of rows in the sheet
        """
        pass

    @abstractmethod
    def number_of_columns(self):
        """
        Number of columns in the sheet
        """
        pass

    @abstractmethod
    def cell_value(self, row, column):
        """
        Random access to the cells
        """
        pass

    def to_array(self):
        array = []
        for r in range(0, self.number_of_rows()):
            row = []
            for c in range(0, self.number_of_columns()):
                row.append(self.cell_value(r, c))
            array.append(row)
        return array


@add_metaclass(ABCMeta)
class BookReaderBase(object):

    @abstractmethod
    def sheets(self):
        """Get sheets in a dictionary"""
        pass


class BookReader(BookReaderBase):
    """
    XLSBook reader

    It reads xls, xlsm, xlsx work book
    """

    def __init__(self, filename, file_content=None,
                 load_sheet_with_name=None,
                 load_sheet_at_index=None,
                 **keywords):
        self.load_from_memory_flag = False
        self.keywords = keywords
        self.sheet_name = load_sheet_with_name
        self.sheet_index = load_sheet_at_index
        if file_content:
            self.load_from_memory_flag = True
            self.native_book = self.load_from_memory(file_content, **keywords)
        else:
            self.native_book = self.load_from_file(filename, **keywords)
        self.mysheets = OrderedDict()
        for native_sheet in self.sheet_iterator():
            sheet = self.get_sheet(native_sheet)
            self.mysheets[sheet.name] = sheet.to_array()

    def set_type(self, file_type):
        self.file_type = file_type

    @abstractmethod
    def sheet_iterator(self):
        pass

    @abstractmethod
    def get_sheet(self, native_sheet, **keywords):
        """Return a context specific sheet from a native sheet
        """
        pass

    @abstractmethod
    def load_from_memory(self, file_content, **keywords):
        """Load content from memory

        :params stream file_content: the actual file content in memory
        :returns: a book
        """
        pass

    @abstractmethod
    def load_from_file(self, filename, **keywords):
        """Load content from a file

        :params str filename: an accessible file path
        :returns: a book
        """
        pass

    def sheets(self):
        """Get sheets in a dictionary"""
        return self.mysheets


@add_metaclass(ABCMeta)
class SheetWriterBase(object):
    @abstractmethod
    def set_size(self, size):
        """size of the content will be given
        """
        pass

    @abstractmethod
    def write_array(self, table):
        """For standalone usage, write an array
        """
        pass

    @abstractmethod
    def close(self):
        """
        This call actually save the file
        """
        pass


@add_metaclass(ABCMeta)
class SheetWriter(SheetWriterBase):
    """
    xls, xlsx and xlsm sheet writer
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
        pass

    def set_size(self, size):
        """size of the content will be given
        """
        pass

    @abstractmethod
    def write_row(self, array):
        """
        write a row into the file
        """
        pass

    def write_array(self, table):
        """For standalone usage, write an array
        """
        for r in table:
            self.write_row(r)

    def close(self):
        """
        This call actually save the file
        """
        pass


@add_metaclass(ABCMeta)
class BookWriter(object):
    """
    xls, xlsx and xlsm writer
    """
    def __init__(self, file, **keywords):
        self.file = file
        self.keywords = keywords

    @abstractmethod
    def create_sheet(self, name):
        """Get a native sheet out"""
        pass

    def set_type(self, file_type):
        self.file_type = file_type

    def write(self, sheet_dicts):
        """Write a dictionary to a multi-sheet file

        Requirements for the dictionary is: key is the sheet name,
        its value must be two dimensional array
        """
        keys = sheet_dicts.keys()
        for name in keys:
            sheet = self.create_sheet(name)
            if sheet is not None:
                sheet.write_array(sheet_dicts[name])
                sheet.close()

    @abstractmethod
    def close(self):
        """
        This call actually save the file
        """
        pass


def from_query_sets(column_names, query_sets):
    array = []
    array.append(column_names)
    for o in query_sets:
        new_array = []
        for column in column_names:
            value = getattr(o, column)
            if isinstance(value, (datetime.date, datetime.time)):
                value = value.isoformat()
            new_array.append(value)
        array.append(new_array)
    return array


def is_empty_array(array):
    return len([x for x in array if x != '']) == 0


def swap_empty_string_for_none(array):
    def swap(x):
        if x == '':
            return None
        else:
            return x
    return [swap(x) for x in array]
