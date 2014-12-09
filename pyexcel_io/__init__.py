"""
    pyexcel.ext.io
    ~~~~~~~~~~~~~~~~~~~

    The io interface to file extensions

    :copyright: (c) 2014 by C. W.
    :license: GPL v3
"""
import sys
from abc import abstractmethod, abstractproperty
if sys.version_info[0] == 2 and sys.version_info[1] < 7:
    from ordereddict import OrderedDict
else:
    from collections import OrderedDict

DEFAULT_SHEETNAME = 'pyexcel_sheet1'

    
class SheetReaderBase(object):
    """
    sheet

    Currently only support first sheet in the file
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

    def __init__(self, filename, file_content=None, **keywords):
        self.load_from_memory_flag = False
        if file_content:
            self.load_from_memory_flag = True
            self.native_book = self.load_from_memory(file_content, **keywords)
        else:
            self.native_book = self.load_from_file(filename, **keywords)
        self.mysheets = OrderedDict()
        for native_sheet in self.sheetIterator():
            sheet = self.getSheet(native_sheet, **keywords)
            self.mysheets[sheet.name] = sheet.to_array()

    @abstractmethod
    def sheetIterator(self):
        pass

    def getSheet(self, native_sheet, **keywords):
        """Return a context specific sheet from a native sheet
        """
        return SheetReader(native_sheet, **keywords)

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


class SheetWriter:
    """
    xls, xlsx and xlsm sheet writer
    """
    def __init__(self, native_book, native_sheet, name, **keywords):
        if name:
            sheet_name = name
        else:
            sheet_name = DEFAULT_SHEETNAME
        self.native_book = native_book
        self.native_sheet = native_sheet
        self.keywords = keywords
        self.set_sheet_name(sheet_name)

    @abstractmethod
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


class BookWriter:
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

    def write(self, sheet_dicts):
        """Write a dictionary to a multi-sheet file

        Requirements for the dictionary is: key is the sheet name,
        its value must be two dimensional array
        """
        keys = sheet_dicts.keys()
        for name in keys:
            sheet = self.create_sheet(name)
            sheet.write_array(sheet_dicts[name])
            sheet.close()

    @abstractmethod
    def close(self):
        """
        This call actually save the file
        """
        pass
