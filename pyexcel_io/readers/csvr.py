"""
    pyexcel_io.readers.csvr
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    csv file reader

    :copyright: (c) 2014-2017 by Onni Software Ltd.
    :license: New BSD License, see LICENSE for more details
"""
import re
import os
import csv
import glob
import codecs
import datetime

from pyexcel_io.book import BookReader
from pyexcel_io.sheet import SheetReader, NamedContent
import pyexcel_io._compact as compact
import pyexcel_io.constants as constants


class UTF8Recorder(compact.Iterator):
    """
    Iterator that reads an encoded stream and reencodes the input to UTF-8.
    """
    def __init__(self, f, encoding):
        self.reader = codecs.getreader(encoding)(f)

    def __iter__(self):
        return self

    def __next__(self):
        return next(self.reader).encode('utf-8')


class CSVSheetReader(SheetReader):
    """ generic csv file reader"""
    def __init__(self, sheet, encoding="utf-8",
                 auto_detect_float=True, ignore_infinity=True,
                 auto_detect_int=True, auto_detect_datetime=True,
                 **keywords):
        SheetReader.__init__(self, sheet, **keywords)
        self._encoding = encoding
        self.__auto_detect_int = auto_detect_int
        self.__auto_detect_float = auto_detect_float
        self.__ignore_infinity = ignore_infinity
        self.__auto_detect_datetime = auto_detect_datetime

    def get_file_handle(self):
        """ return me unicde reader for csv """
        raise NotImplementedError("Please implement get_file_handle()")

    def row_iterator(self):
        return csv.reader(self.get_file_handle(), **self._keywords)

    def column_iterator(self, row):
        for element in row:
            if compact.PY2:
                element = element.decode('utf-8')
            if element is not None and element != '':
                element = self.__convert_cell(element)
            yield element

    def __convert_cell(self, csv_cell_text):
        ret = None
        if self.__auto_detect_int:
            ret = _detect_int_value(csv_cell_text)
        if ret is None and self.__auto_detect_float:
            ret = _detect_float_value(csv_cell_text)
            shall_we_ignore_the_conversion = (
                (ret in [float('inf'), float('-inf')]) and
                self.__ignore_infinity
            )
            if shall_we_ignore_the_conversion:
                ret = None
        if ret is None and self.__auto_detect_datetime:
            ret = _detect_date_value(csv_cell_text)
        if ret is None:
            ret = csv_cell_text
        return ret


class CSVFileReader(CSVSheetReader):
    """ read csv from phyical file """
    def get_file_handle(self):
        unicode_reader = None
        if compact.PY2:
            file_handle = open(self._native_sheet.payload, 'rb')
            unicode_reader = UTF8Recorder(file_handle, self._encoding)
        else:
            unicode_reader = open(self._native_sheet.payload, 'r',
                                  encoding=self._encoding)
        return unicode_reader


class CSVinMemoryReader(CSVSheetReader):
    """ read csv file from memory """
    def get_file_handle(self):
        unicode_reader = None
        if compact.PY2:
            unicode_reader = UTF8Recorder(self._native_sheet.payload,
                                          self._encoding)
        else:
            if isinstance(self._native_sheet.payload, compact.BytesIO):
                content = self._native_sheet.payload.read()
                unicode_reader = compact.StringIO(
                    content.decode(self._encoding))
            else:
                unicode_reader = self._native_sheet.payload

        return unicode_reader


class CSVBookReader(BookReader):
    """ read csv file """
    def __init__(self):
        BookReader.__init__(self)
        self._file_type = constants.FILE_FORMAT_CSV
        self.__load_from_memory_flag = False
        self.__line_terminator = constants.DEFAULT_CSV_NEWLINE
        self.__sheet_name = None
        self.__sheet_index = None

    def open(self, file_name, **keywords):
        BookReader.open(self, file_name, **keywords)
        self._native_book = self._load_from_file()

    def open_stream(self, file_stream, **keywords):
        BookReader.open_stream(self, file_stream, **keywords)
        self._native_book = self._load_from_stream()

    def read_sheet(self, native_sheet):
        if self.__load_from_memory_flag:
            reader = CSVinMemoryReader(native_sheet, **self._keywords)
        else:
            reader = CSVFileReader(native_sheet, **self._keywords)
        return reader.to_array()

    def _load_from_stream(self):
        """Load content from memory

        :params stream file_content: the actual file content in memory
        :returns: a book
        """
        self.__line_terminator = self._keywords.get(
            constants.KEYWORD_LINE_TERMINATOR,
            self.__line_terminator)
        self.__load_from_memory_flag = True
        self._file_stream.seek(0)
        content = self._file_stream.read()
        separator = constants.SEPARATOR_FORMATTER % self.__line_terminator
        if separator in content:
            sheets = content.split(separator)
            named_contents = []
            for sheet in sheets:
                if sheet == '':  # skip empty named sheet
                    continue
                lines = sheet.split(self.__line_terminator)
                result = re.match(constants.SEPARATOR_MATCHER, lines[0])
                new_content = '\n'.join(lines[1:])
                new_sheet = NamedContent(result.group(1),
                                         compact.StringIO(new_content))
                named_contents.append(new_sheet)
            return named_contents
        else:
            self._file_stream.seek(0)
            return [NamedContent(self._file_type, self._file_stream)]

    def _load_from_file(self):
        """Load content from a file

        :params str filename: an accessible file path
        :returns: a book
        """
        self.__line_terminator = self._keywords.get(
            constants.KEYWORD_LINE_TERMINATOR,
            self.__line_terminator)
        names = self._file_name.split('.')
        filepattern = "%s%s*%s*.%s" % (
            names[0],
            constants.DEFAULT_MULTI_CSV_SEPARATOR,
            constants.DEFAULT_MULTI_CSV_SEPARATOR,
            names[1])
        filelist = glob.glob(filepattern)
        if len(filelist) == 0:
            file_parts = os.path.split(self._file_name)
            return [NamedContent(file_parts[-1], self._file_name)]
        else:
            matcher = "%s%s(.*)%s(.*).%s" % (
                names[0],
                constants.DEFAULT_MULTI_CSV_SEPARATOR,
                constants.DEFAULT_MULTI_CSV_SEPARATOR,
                names[1])
            tmp_file_list = []
            for filen in filelist:
                result = re.match(matcher, filen)
                tmp_file_list.append((result.group(1), result.group(2), filen))
            ret = []
            for lsheetname, index, filen in sorted(tmp_file_list,
                                                   key=lambda row: row[1]):
                ret.append(NamedContent(lsheetname, filen))
            return ret


def _detect_date_value(csv_cell_text):
    """
    Read the date formats that were written by csv.writer
    """
    ret = None
    try:
        if len(csv_cell_text) == 10:
            ret = datetime.datetime.strptime(
                csv_cell_text,
                "%Y-%m-%d")
            ret = ret.date()
        elif len(csv_cell_text) == 19:
            ret = datetime.datetime.strptime(
                csv_cell_text,
                "%Y-%m-%d %H:%M:%S")
        elif len(csv_cell_text) > 19:
            ret = datetime.datetime.strptime(
                csv_cell_text[0:26],
                "%Y-%m-%d %H:%M:%S.%f")
    except ValueError:
        pass
    return ret


def _detect_float_value(csv_cell_text):
    try:
        if csv_cell_text.startswith('0'):
            # do not convert if a number starts with 0
            # e.g. 014325
            return None
        else:
            return float(csv_cell_text)
    except ValueError:
        return None


def _detect_int_value(csv_cell_text):
    if csv_cell_text.startswith('0') and len(csv_cell_text) > 1:
        return None
    try:
        return int(csv_cell_text)
    except ValueError:
        return None
