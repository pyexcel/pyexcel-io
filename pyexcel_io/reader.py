from pyexcel_io import exceptions
from pyexcel_io.book import _convert_content_to_stream
from pyexcel_io.sheet import SheetReader
from pyexcel_io.plugins import NEW_READERS
from pyexcel_io._compact import OrderedDict


def clean_keywords(keywords):
    sheet_keywords = {}
    native_sheet_keywords = {}
    args_list = [
        "start_row",
        "row_limit",
        "start_column",
        "column_limit",
        "skip_column_func",
        "skip_row_func",
        "skip_empty_rows",
        "row_renderer",
    ]
    for arg in keywords:
        if arg in args_list:
            sheet_keywords[arg] = keywords[arg]
        else:
            native_sheet_keywords[arg] = keywords[arg]
    return sheet_keywords, native_sheet_keywords


class Reader(object):
    def __init__(self, file_type, library=None):
        self.file_type = file_type
        self.library = library
        self.keywords = None

    def open(self, file_name, **keywords):
        self.reader = NEW_READERS.get_a_plugin(
            self.file_type, location="file", library=self.library
        )
        self.keywords, native_sheet_keywords = clean_keywords(keywords)
        return self.reader.open(file_name, **native_sheet_keywords)

    def open_content(self, file_content, **keywords):
        self.keywords, native_sheet_keywords = clean_keywords(keywords)
        try:
            self.reader = NEW_READERS.get_a_plugin(
                self.file_type, location="content", library=self.library
            )
            return self.reader.open(file_content, **native_sheet_keywords)
        except (
            exceptions.NoSupportingPluginFound,
            exceptions.SupportingPluginAvailableButNotInstalled,
        ):
            file_stream = _convert_content_to_stream(
                file_content, self.file_type
            )
            return self.open_stream(file_stream, **native_sheet_keywords)

    def open_stream(self, file_stream, **keywords):
        self.keywords, native_sheet_keywords = clean_keywords(keywords)
        self.reader = NEW_READERS.get_a_plugin(
            self.file_type, location="memory", library=self.library
        )
        return self.reader.open(file_stream, **native_sheet_keywords)

    def read_sheet_by_name(self, sheet_name):
        """
        read a named sheet from a excel data book
        """
        for index, content in enumerate(self.reader.content_array):
            if content.name == sheet_name:
                return {content.name: self.read_sheet(index)}
        else:
            raise ValueError("Cannot find sheet %s" % sheet_name)

    def read_sheet(self, sheet_index):
        sheet_reader = self.reader.read_sheet(sheet_index)
        sheet = EncapsulatedSheetReader(sheet_reader, **self.keywords)
        return sheet.to_array()

    def read_sheet_by_index(self, sheet_index):
        """
        read an indexed sheet from a excel data book
        """
        try:
            name = self.reader.content_array[sheet_index].name
            return {name: self.read_sheet(sheet_index)}

        except IndexError:
            self.close()
            raise

    def read_all(self):
        """
        read everything from a excel data book
        """
        result = OrderedDict()
        for index, sheet in enumerate(self.reader.content_array):
            result.update(
                {self.reader.content_array[index].name: self.read_sheet(index)}
            )
        return result

    def read_many(self, sheets):
        """
        read everything from a excel data book
        """
        result = OrderedDict()
        for sheet in sheets:
            if isinstance(sheet, int):
                result.update(self.read_sheet_by_index(sheet))
            else:
                result.update(self.read_sheet_by_name(sheet))
        return result

    def close(self):
        return self.reader.close()

    def __enter__(self):
        return self

    def __exit__(self, a_type, value, traceback):
        self.close()


class EncapsulatedSheetReader(SheetReader):
    def row_iterator(self):
        yield from self._native_sheet.row_iterator()

    def column_iterator(self, row):
        yield from self._native_sheet.column_iterator(row)
