"""
    pyexcel.ioext
    ~~~~~~~~~~~~~~~~~~~

    The io interface to file extensions

    :copyright: (c) 2014 by C. W.
    :license: GPL v3
"""
import sys
from abc import abstractmethod
if sys.version_info[0] == 2 and sys.version_info[1] < 7:
    from ordereddict import OrderedDict
else:
    from collections import OrderedDict


class SheetReaderBase(object):
    """
    sheet

    Currently only support first sheet in the file
    """
    def __init__(self, sheet):
        self.native_sheet = sheet

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


class BookReader(object):
    """
    XLSBook reader

    It reads xls, xlsm, xlsx work book
    """

    def __init__(self, filename, file_content=None, **keywords):
        if file_content:
            self.native_book = self.load_from_memory(file_content)
        else:
            self.native_book = self.load_from_file(filename)
        self.mysheets = OrderedDict()
        for native_sheet in self.sheetIterator():
            sheet = self.getSheet(native_sheet)
            self.mysheets[sheet.name] = sheet.to_array()

    @abstractmethod
    def sheetIterator(self):
        pass

    def getSheet(self, nativeSheet):
        """Return a context specific sheet from a native sheet
        """
        return SheetReader(nativeSheet)

    @abstractmethod
    def load_from_memory(self, file_content):
        """Load content from memory

        :params stream file_content: the actual file content in memory
        :returns: a book
        """
        pass

    @abstractmethod
    def load_from_file(self, filename):
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
    def __init__(self, native_book, native_sheet, name):
        if name:
            sheet_name = name
        else:
            sheet_name = "pyexcel_sheet1"
        self.native_book = native_book
        self.native_sheet = native_sheet
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
    def __init__(self, file):
        self.file = file

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
