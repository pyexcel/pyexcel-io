"""
    pyexcel_io.csvbook
    ~~~~~~~~~~~~~~~~~~~

    The lower level csv file format handler.

    :copyright: (c) 2014-2016 by Onni Software Ltd.
    :license: New BSD License, see LICENSE for more details
"""
import re
import os
import csv
import codecs
import glob
from abc import abstractmethod
from .base import (
    BookReader,
    SheetReaderBase,
    SheetWriter,
    BookWriter,
    NamedContent
)
from ._compact import (
    is_string,
    StringIO,
    BytesIO,
    PY2,
    text_type,
    Iterator,
    isstream
)
from .constants import DEFAULT_SEPARATOR, DEFAULT_SHEET_NAME


class UTF8Recorder(Iterator):
    """
    Iterator that reads an encoded stream and reencodes the input to UTF-8.
    """
    def __init__(self, f, encoding):
        self.reader = codecs.getreader(encoding)(f)

    def __iter__(self):
        return self

    def __next__(self):
        return next(self.reader).encode('utf-8')


class CSVSheetReader(SheetReaderBase):
    def __init__(self, sheet, encoding="utf-8", **keywords):
        SheetReaderBase.__init__(self, sheet, **keywords)
        self.encoding = encoding

    @property
    def name(self):
        return self.native_sheet.name

    @abstractmethod
    def get_file_handle(self):
        pass

    def to_array(self):
        reader = csv.reader(self.get_file_handle(), **self.keywords)
        for row in reader:
            myrow = []
            tmp_row = []
            for element in row:
                if PY2:
                    element = element.decode(self.encoding)
                tmp_row.append(element)
                if element is not None and element != '':
                    myrow += tmp_row
                    tmp_row = []
            yield myrow


class CSVFileReader(CSVSheetReader):
    def get_file_handle(self):
        if PY2:
            f1 = open(self.native_sheet.payload, 'rb')
            f = UTF8Recorder(f1, self.encoding)
        else:
            f = open(self.native_sheet.payload, 'r')
        return f


class CSVinMemoryReader(CSVSheetReader):
    def get_file_handle(self):
        if PY2:
            f = UTF8Recorder(self.native_sheet.payload,
                             self.encoding)
        else:
            f = self.native_sheet.payload
        return f


class CSVSheetWriter(SheetWriter):
    """
    csv file writer

    """
    def __init__(self, filename, name,
                 encoding="utf-8", single_sheet_in_book=False,
                 sheet_index=None, **keywords):
        self.encoding = encoding
        sheet_name = name
        self.single_sheet_in_book = single_sheet_in_book
        self.line_terminator = '\r\n'
        if 'lineterminator' in keywords:
            self.line_terminator = keywords['lineterminator']
        if single_sheet_in_book:
            sheet_name = None
        elif isstream(filename):
            filename.write("---pyexcel:%s---%s" % (sheet_name, self.line_terminator))
        self.sheet_index = sheet_index
        SheetWriter.__init__(self, filename,
                             sheet_name, sheet_name,
                             **keywords)

    def set_sheet_name(self, name):
        if is_string(type(self.native_book)):
            if name != DEFAULT_SHEET_NAME:
                names = self.native_book.split(".")
                file_name = "%s%s%s%s%s.%s" % (names[0],
                                               DEFAULT_SEPARATOR,
                                               name,              # sheet name
                                               DEFAULT_SEPARATOR,
                                               self.sheet_index,  # sheet index
                                               names[1])
            else:
                file_name = self.native_book
            if PY2:
                self.f = open(file_name, "wb")
            else:
                self.f = open(file_name, "w", newline="")
        else:
            self.f = self.native_book
        self.writer = csv.writer(self.f, **self.keywords)

    def write_row(self, array):
        """
        write a row into the file
        """
        if PY2:
            self.writer.writerow(
                [text_type(s if s is not None else '').encode(self.encoding)
                 for s in array])
        else:
            self.writer.writerow(array)

    def close(self):
        """
        This call close the file handle
        """
        if not (isinstance(self.f, StringIO) or isinstance(self.f, BytesIO)):
            self.f.close()
        elif not self.single_sheet_in_book:
            self.f.write("---pyexcel---%s" % self.line_terminator)


class CSVWriter(BookWriter):
    """
    csv file writer

    if there is multiple sheets for csv file, it simpily writes
    multiple csv files
    """
    def __init__(self, file, **keywords):
        self.index = 0
        BookWriter.__init__(self, file, **keywords)

    def create_sheet(self, name):
        self.index = self.index + 1
        return CSVSheetWriter(self.file, name,
                              sheet_index=(self.index-1),
                              **self.keywords)

    def close(self):
        """
        This call close the file handle
        """
        pass
