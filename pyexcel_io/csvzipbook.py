"""
    pyexcel_io.csvzipbook
    ~~~~~~~~~~~~~~~~~~~

    The lower level csv file format handler.

    :copyright: (c) 2014-2016 by Onni Software Ltd.
    :license: New BSD License, see LICENSE for more details
"""
import csv
import zipfile
from .base import BookReader, BookWriter
from ._compact import StringIO, PY2
from .csvbook import (
    CSVinMemoryReader,
    NamedContent,
    CSVSheetWriter,
)
from .constants import DEFAULT_SHEET_NAME, FILE_FORMAT_CSV, FILE_FORMAT_TSV



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


class CSVZipWriter(BookWriter):
    """
    csv file writer

    if there is multiple sheets for csv file, it simpily writes
    multiple csv files
    """
    def __init__(self, filename, **keywords):
        BookWriter.__init__(self, filename, **keywords)
        self.myzip = zipfile.ZipFile(self.file, 'w')
        if 'dialect' in keywords:
            self.file_extension = FILE_FORMAT_TSV
        else:
            self.file_extension = FILE_FORMAT_CSV

    def create_sheet(self, name):
        given_name = name
        if given_name is None:
            given_name = DEFAULT_SHEET_NAME
        return CSVZipSheetWriter(self.myzip,
                                 given_name,
                                 self.file_extension,
                                 **self.keywords)

    def close(self):
        """
        This call close the file handle
        """
        self.myzip.close()
