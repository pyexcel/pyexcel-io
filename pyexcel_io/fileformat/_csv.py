"""
    pyexcel_io._csv
    ~~~~~~~~~~~~~~~~~~~

    The lower level csv file format handler.

    :copyright: (c) 2014-2016 by Onni Software Ltd.
    :license: New BSD License, see LICENSE for more details
"""
import re
import os
import csv
import glob
import math
import codecs
import datetime

from ..book import BookReader, BookWriter
from ..sheet import SheetReader, SheetWriter, NamedContent
from .._compact import (
    is_string,
    StringIO,
    PY2,
    text_type,
    Iterator,
    isstream
)
from ..constants import (
    DEFAULT_SHEET_NAME,
    FILE_FORMAT_CSV,
    DEFAULT_NAME,
    KEYWORD_LINE_TERMINATOR
)


DEFAULT_SEPARATOR = '__'
DEFAULT_SHEET_SEPARATOR_FORMATTER = '---%s---' % DEFAULT_NAME + "%s"
SEPARATOR_MATCHER = "---%s:(.*)---" % DEFAULT_NAME
DEFAULT_CSV_STREAM_FILE_FORMATTER = "---%s:" % DEFAULT_NAME + "%s---%s"


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


class CSVSheetReader(SheetReader):
    def __init__(self, sheet, encoding="utf-8",
                 auto_detect_float=True, auto_detect_int=True,
                 auto_detect_datetime=True,
                 **keywords):
        SheetReader.__init__(self, sheet, **keywords)
        self.encoding = encoding
        self.auto_detect_int = auto_detect_int
        self.auto_detect_float = auto_detect_float
        self.auto_detect_datetime = auto_detect_datetime

    def get_file_handle(self):
        raise NotImplementedError("Please implement get_file_handle()")

    def to_array(self):
        reader = csv.reader(self.get_file_handle(), **self.keywords)
        for row in reader:
            myrow = []
            tmp_row = []
            for element in row:
                if PY2:
                    element = element.decode(self.encoding)
                if element is not None and element != '':
                    element = self._convert_cell(element)
                tmp_row.append(element)
                if element is not None and element != '':
                    myrow += tmp_row
                    tmp_row = []
            yield myrow

    def _convert_cell(self, csv_cell_text):
        ret = None
        if self.auto_detect_float:
            ret = _detect_float_value(csv_cell_text)
            if ret is not None and self.auto_detect_int:
                if ret == math.floor(ret):
                    ret = int(ret)
        if ret is None and self.auto_detect_datetime:
            ret = _detect_date_value(csv_cell_text)
        if ret is None:
            return csv_cell_text
        else:
            return ret


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
        if KEYWORD_LINE_TERMINATOR in keywords:
            self.line_terminator = keywords[KEYWORD_LINE_TERMINATOR]
        if single_sheet_in_book:
            sheet_name = None
        elif isstream(filename):
            filename.write(DEFAULT_CSV_STREAM_FILE_FORMATTER % (
                sheet_name,
                self.line_terminator))
        self.sheet_index = sheet_index
        SheetWriter.__init__(self, filename,
                             sheet_name, sheet_name,
                             **keywords)

    def set_sheet_name(self, name):
        if is_string(type(self.native_book)):
            if name != DEFAULT_SHEET_NAME:
                names = self.native_book.split(".")
                file_name = "%s%s%s%s%s.%s" % (
                    names[0],
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
        if not isstream(self.f):
            self.f.close()
        elif not self.single_sheet_in_book:
            self.f.write(
                DEFAULT_SHEET_SEPARATOR_FORMATTER % self.line_terminator)


class CSVBookReader(BookReader):
    def __init__(self):
        BookReader.__init__(self)
        self.file_type = FILE_FORMAT_CSV
        self.load_from_memory_flag = False
        self.line_terminator = '\r\n'
        self.sheet_name = None
        self.sheet_index = None

    def open(self, file_name, **keywords):
        BookReader.open(self, file_name, **keywords)
        self.native_book = self._load_from_file()

    def open_stream(self, file_stream, **keywords):
        BookReader.open_stream(self, file_stream, **keywords)
        self.native_book = self._load_from_stream()

    def read_sheet(self, native_sheet):
        if self.load_from_memory_flag:
            reader = CSVinMemoryReader(native_sheet, **self.keywords)
        else:
            reader = CSVFileReader(native_sheet, **self.keywords)
        return reader.to_array()

    def _load_from_stream(self):
        """Load content from memory

        :params stream file_content: the actual file content in memory
        :returns: a book
        """
        if KEYWORD_LINE_TERMINATOR in self.keywords:
            self.line_terminator = self.keywords[KEYWORD_LINE_TERMINATOR]
        self.load_from_memory_flag = True
        content = self.file_stream.getvalue()
        separator = DEFAULT_SHEET_SEPARATOR_FORMATTER % self.line_terminator
        if separator in content:
            sheets = content.split(separator)
            named_contents = []
            for sheet in sheets:
                if sheet == '':  # skip empty named sheet
                    continue
                lines = sheet.split(self.line_terminator)
                result = re.match(SEPARATOR_MATCHER, lines[0])
                new_content = '\n'.join(lines[1:])
                new_sheet = NamedContent(result.group(1),
                                         StringIO(new_content))
                named_contents.append(new_sheet)
            return named_contents
        else:
            self.file_stream.seek(0)
            return [NamedContent(self.file_type, self.file_stream)]

    def _load_from_file(self):
        """Load content from a file

        :params str filename: an accessible file path
        :returns: a book
        """
        if KEYWORD_LINE_TERMINATOR in self.keywords:
            self.line_terminator = self.keywords[KEYWORD_LINE_TERMINATOR]
        names = self.file_name.split('.')
        filepattern = "%s%s*%s*.%s" % (
            names[0],
            DEFAULT_SEPARATOR,
            DEFAULT_SEPARATOR,
            names[1])
        filelist = glob.glob(filepattern)
        if len(filelist) == 0:
            file_parts = os.path.split(self.file_name)
            return [NamedContent(file_parts[-1], self.file_name)]
        else:
            matcher = "%s%s(.*)%s(.*).%s" % (
                names[0],
                DEFAULT_SEPARATOR,
                DEFAULT_SEPARATOR,
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


class CSVBookWriter(BookWriter):
    def __init__(self):
        BookWriter.__init__(self)
        self.file_type = FILE_FORMAT_CSV
        self.index = 0

    def create_sheet(self, name):
        writer = CSVSheetWriter(
            self.file_alike_object,
            name,
            sheet_index=self.index,
            **self.keywords)
        self.index = self.index + 1
        return writer


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


_registry = {
    "file_type": FILE_FORMAT_CSV,
    "reader": CSVBookReader,
    "writer": CSVBookWriter,
    "stream_type": "text",
    "mime_type": "text/csv",
    "library": "built-in"
}

exports = (_registry,)
