import re

import pyexcel_io._compact as compact
from pyexcel_io import constants
from pyexcel_io.sheet import NamedContent
from pyexcel_io.readers.csvr import CSVinMemoryReader

DEFAULT_SHEET_SEPARATOR_FORMATTER = f"---{constants.DEFAULT_NAME}---%s"


class MemoryReader(object):
    def __init__(self):
        self.handles = []
        self.file_type = constants.FILE_FORMAT_CSV

    def set_type(self, _):
        pass

    def open(self, file_stream, multiple_sheets=False, **keywords):
        """Load content from memory
        :params stream file_content: the actual file content in memory
        :returns: a book
        """
        self.keywords = keywords
        self.__load_from_memory_flag = True
        self.__line_terminator = keywords.get(
            constants.KEYWORD_LINE_TERMINATOR, constants.DEFAULT_CSV_NEWLINE
        )
        separator = DEFAULT_SHEET_SEPARATOR_FORMATTER % self.__line_terminator
        if multiple_sheets:
            # will be slow for large files
            file_stream.seek(0)
            content = file_stream.read()
            sheets = content.split(separator)
            named_contents = []
            for sheet in sheets:
                if sheet == "":  # skip empty named sheet
                    continue

                lines = sheet.split(self.__line_terminator)
                result = re.match(constants.SEPARATOR_MATCHER, lines[0])
                new_content = "\n".join(lines[1:])
                new_sheet = NamedContent(
                    result.group(1), compact.StringIO(new_content)
                )
                named_contents.append(new_sheet)
            self.content_array = named_contents

        else:
            if hasattr(file_stream, "seek"):
                file_stream.seek(0)
            self.content_array = [NamedContent(self.file_type, file_stream)]

    def read_sheet(self, index):
        return CSVinMemoryReader(self.content_array[index], **self.keywords)

    def close(self):
        for reader in self.handles:
            reader.close()
