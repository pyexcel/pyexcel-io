from ..manager import RWManager
from ..constants import (
    FILE_FORMAT_TSVZ,
    KEYWORD_TSV_DIALECT
)

from .csvz import CSVZipBookReader, CSVZipBookWriter


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


class TSVZipBookWriter(CSVZipBookWriter):
    def __init__(self):
        CSVZipBookWriter.__init__(self)
        self.file_type = FILE_FORMAT_TSVZ

    def open(self, file_name, **keywords):
        keywords['dialect'] = KEYWORD_TSV_DIALECT
        CSVZipBookWriter.open(self, file_name, **keywords)


RWManager.register_a_reader(FILE_FORMAT_TSVZ, TSVZipBookReader)
RWManager.register_a_writer(FILE_FORMAT_TSVZ, TSVZipBookWriter)
RWManager.register_file_type_as_binary_stream(FILE_FORMAT_TSVZ)
