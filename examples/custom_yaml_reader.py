import yaml
from pyexcel_io import get_data
from pyexcel_io.sheet import NamedContent
from pyexcel_io.plugins import IOPluginInfoChainV2
from pyexcel_io.plugin_api import ISheet, IReader


class YourSingleSheet(ISheet):
    def __init__(self, your_native_sheet):
        self.two_dimensional_array = your_native_sheet

    def row_iterator(self):
        yield from self.two_dimensional_array

    def column_iterator(self, row):
        yield from row


class YourReader(IReader):
    def __init__(self, file_name, file_type, **keywords):
        self.file_handle = open(file_name, "r")
        self.native_book = yaml.load(self.file_handle)
        self.content_array = [
            NamedContent(key, values)
            for key, values in self.native_book.items()
        ]

    def read_sheet(self, sheet_index):
        two_dimensional_array = self.content_array[sheet_index].payload
        return YourSingleSheet(two_dimensional_array)

    def close(self):
        self.file_handle.close()


IOPluginInfoChainV2(__name__).add_a_reader(
    relative_plugin_class_path="YourReader",
    locations=["file"],
    file_types=["yaml"],
    stream_type="text",
)

if __name__ == "__main__":
    data = get_data("test.yaml")
    print(data)
