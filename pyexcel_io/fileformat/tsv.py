"""
    pyexcel_io.fileformat.tsv
    ~~~~~~~~~~~~~~~~~~~

    The lower level tsv file format handler.

    :copyright: (c) 2014-2016 by Onni Software Ltd.
    :license: New BSD License, see LICENSE for more details
"""
from ..manager import RWManager
from ..constants import (
    FILE_FORMAT_TSV,
    KEYWORD_TSV_DIALECT
)

from .csv import CSVBookReader, CSVBookWriter

class TSVBookReader(CSVBookReader):
    def __init__(self):
        CSVBookReader.__init__(self)
        self.file_type = FILE_FORMAT_TSV

    def open(self, file_name, **keywords):
        keywords['dialect'] = KEYWORD_TSV_DIALECT
        CSVBookReader.open(self, file_name, **keywords)

    def open_stream(self, file_content, **keywords):
        keywords['dialect'] = KEYWORD_TSV_DIALECT
        CSVBookReader.open_stream(self, file_content, **keywords)


class TSVBookWriter(CSVBookWriter):
    def __init__(self):
        CSVBookWriter.__init__(self)
        self.file_type = FILE_FORMAT_TSV

    def open(self, file_name, **keywords):
        keywords['dialect'] = KEYWORD_TSV_DIALECT
        CSVBookWriter.open(self, file_name, **keywords)


RWManager.register_a_reader(FILE_FORMAT_TSV, CSVBookReader)
RWManager.register_a_writer(FILE_FORMAT_TSV, CSVBookWriter)
RWManager.register_file_type_as_text_stream(FILE_FORMAT_TSV)
