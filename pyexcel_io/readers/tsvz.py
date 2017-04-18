"""
    pyexcel_io.fileformat.tsvz
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    The lower level tsvz file format handler.

    :copyright: (c) 2014-2017 by Onni Software Ltd.
    :license: New BSD License, see LICENSE for more details
"""
from pyexcel_io.constants import (
    FILE_FORMAT_TSVZ,
    KEYWORD_TSV_DIALECT
)

from .csvz import CSVZipBookReader


class TSVZipBookReader(CSVZipBookReader):
    file_types = [FILE_FORMAT_TSVZ]

    def __init__(self):
        CSVZipBookReader.__init__(self)
        self._file_type = FILE_FORMAT_TSVZ

    def open(self, file_name, **keywords):
        keywords['dialect'] = KEYWORD_TSV_DIALECT
        CSVZipBookReader.open(self, file_name, **keywords)

    def open_stream(self, file_content, **keywords):
        keywords['dialect'] = KEYWORD_TSV_DIALECT
        CSVZipBookReader.open_stream(self, file_content, **keywords)
