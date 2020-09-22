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
    def __init__(self, file_name, **keywords):
        super().__init__(
            file_name, dialect=constants.KEYWORD_TSV_DIALECT, **keywords
        )


class TSVMemoryReader(MemoryReader):
    file_type = constants.FILE_FORMAT_TSV

    def __init__(self, file_stream, **keywords):
        super().__init__(
            file_stream, dialect=constants.KEYWORD_TSV_DIALECT, **keywords
        )


class TSVContentReader(ContentReader):
    file_type = constants.FILE_FORMAT_TSV

    def __init__(self, file_content, **keywords):
        super().__init__(
            file_stream, dialect=constants.KEYWORD_TSV_DIALECT, **keywords
        )
