"""
    pyexcel_io.readers.tsv
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    The lower level tsv file format handler.

    :copyright: (c) 2014-2020 by Onni Software Ltd.
    :license: New BSD License, see LICENSE for more details
"""
import pyexcel_io.constants as constants
from pyexcel_io.readers.csv_file_reader import FileReader
from pyexcel_io.readers.csv_memory_reader import MemoryReader
from pyexcel_io.readers.csv_content_reader import ContentReader


class TSVFileReader(FileReader):
    def open(self, file_name, **keywords):
        keywords["dialect"] = constants.KEYWORD_TSV_DIALECT
        super(TSVFileReader, self).open(file_name, **keywords)


class TSVMemoryReader(MemoryReader):
    def __init__(self):
        self.handles = []
        self.file_type = constants.FILE_FORMAT_TSV

    def open(self, file_stream, **keywords):
        keywords["dialect"] = constants.KEYWORD_TSV_DIALECT
        super(TSVMemoryReader, self).open(file_stream, **keywords)


class TSVContentReader(ContentReader):
    def __init__(self):
        self.handles = []
        self.file_type = constants.FILE_FORMAT_TSV

    def open(self, file_content, **keywords):
        keywords["dialect"] = constants.KEYWORD_TSV_DIALECT
        super(TSVContentReader, self).open(file_content, **keywords)
