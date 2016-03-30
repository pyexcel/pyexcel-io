"""
    pyexcel_io.csvzipbook
    ~~~~~~~~~~~~~~~~~~~

    The lower level csv file format handler.

    :copyright: (c) 2014-2016 by Onni Software Ltd.
    :license: New BSD License, see LICENSE for more details
"""
import csv
import zipfile

from ._compact import StringIO, PY2
from .book import BookReader, BookWriter
from .csvbook import (
    CSVinMemoryReader,
    NamedContent,
    CSVSheetWriter,
)
from .manager import RWManager
from .constants import (
    DEFAULT_SHEET_NAME, FILE_FORMAT_CSVZ, FILE_FORMAT_TSVZ,
    KEYWORD_TSV_DIALECT
)


class CSVZipSheetWriter(CSVSheetWriter):
    def __init__(self, zipfile, sheetname, file_extension, **keywords):
        self.file_extension = file_extension
        keywords['single_sheet_in_book'] = False
        CSVSheetWriter.__init__(self, zipfile, sheetname, **keywords)

    def set_sheet_name(self, name):
        self.content = StringIO()
        self.writer = csv.writer(self.content, **self.keywords)

    def close(self):
        file_name = "%s.%s" % (self.native_sheet, self.file_extension)
        self.native_book.writestr(file_name, self.content.getvalue())
        self.content.close()


class CSVZipBookReader(BookReader):
    def __init__(self):
        BookReader.__init__(self, FILE_FORMAT_CSVZ)
        self.zipfile = None

    def load_from_stream(self, file_content):
        self.zipfile = zipfile.ZipFile(file_content, 'r')
        sheets = [NamedContent(self._get_sheet_name(name), name)
                  for name in self.zipfile.namelist()]
        return sheets

    def load_from_file(self, file_name):
        return self.load_from_stream(file_name)

    def read_sheet(self, native_sheet):
        content = self.zipfile.read(native_sheet.payload)
        if PY2:
            sheet = StringIO(content)
        else:
            sheet = StringIO(content.decode('utf-8'))

        reader = CSVinMemoryReader(
            NamedContent(
                native_sheet.name,
                sheet
            ),
            **self.keywords
        )
        return reader.to_array()

    def _get_sheet_name(self, filename):
        len_of_a_dot = 1
        len_of_csv_word = 3
        name_len = len(filename) - len_of_a_dot - len_of_csv_word
        return filename[:name_len]

    def close(self):
        self.zipfile.close()


class TSVZipBookReader(CSVZipBookReader):
    def __init__(self):
        CSVZipBookReader.__init__(self)
        self.file_type = FILE_FORMAT_TSVZ

    def open(self, file_name, **keywords):
        keywords['dialect'] = KEYWORD_TSV_DIALECT
        CSVZipBookReader.open(self, file_name, **keywords)

    def open_stream(self, file_content, **keywords):
        keywords['dialect'] = KEYWORD_TSV_DIALECT
        CSVZipBookReader.open_stream(self, file_content, **keywords)


class CSVZipBookWriter(BookWriter):
    def __init__(self):
        BookWriter.__init__(self, FILE_FORMAT_CSVZ)
        self.zipfile = None

    def open(self, file_name, **keywords):
        BookWriter.open(self, file_name, **keywords)
        self.zipfile = zipfile.ZipFile(file_name, 'w')

    def create_sheet(self, name):
        given_name = name
        if given_name is None:
            given_name = DEFAULT_SHEET_NAME
        writer = CSVZipSheetWriter(
            self.zipfile,
            given_name,
            self.file_type[:3],
            **self.keywords
        )
        return writer

    def close(self):
        self.zipfile.close()


class TSVZipBookWriter(CSVZipBookWriter):
    def __init__(self):
        CSVZipBookWriter.__init__(self)
        self.file_type = FILE_FORMAT_TSVZ

    def open(self, file_name, **keywords):
        keywords['dialect'] = KEYWORD_TSV_DIALECT
        CSVZipBookWriter.open(self, file_name, **keywords)


RWManager.register_readers({
    FILE_FORMAT_CSVZ: CSVZipBookReader,
    FILE_FORMAT_TSVZ: TSVZipBookReader
})
RWManager.register_writers({
    FILE_FORMAT_CSVZ: CSVZipBookWriter,
    FILE_FORMAT_TSVZ: TSVZipBookWriter
})
RWManager.register_file_type_as_binary_stream(FILE_FORMAT_CSVZ)
RWManager.register_file_type_as_binary_stream(FILE_FORMAT_TSVZ)
