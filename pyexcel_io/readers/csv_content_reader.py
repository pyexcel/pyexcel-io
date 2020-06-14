import mmap

from pyexcel_io import constants
from pyexcel_io.book import _convert_content_to_stream
from pyexcel_io.readers.csvr import CSVMemoryMapIterator
from pyexcel_io.readers.csv_memory_reader import MemoryReader


class ContentReader(MemoryReader):
    def open(self, file_content, **keywords):
        encoding = keywords.get("encoding", "utf-8")
        if isinstance(file_content, mmap.mmap):
            # load from mmap
            file_stream = CSVMemoryMapIterator(file_content, encoding)
        else:
            if isinstance(file_content, bytes):
                file_content = file_content.decode(encoding)

            file_stream = _convert_content_to_stream(
                file_content, constants.FILE_FORMAT_CSV
            )
        super(ContentReader, self).open(file_stream, **keywords)
