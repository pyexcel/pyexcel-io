import yaml
from pyexcel_io import save_data
from pyexcel_io.plugins import IOPluginInfoChainV2
from pyexcel_io.plugin_api import IWriter, ISheetWriter


class MySheetWriter(ISheetWriter):
    def __init__(self, sheet_reference):
        self.native_sheet = sheet_reference

    def write_row(self, data_row):
        self.native_sheet.append(data_row)

    def close(self):
        pass


class MyWriter(IWriter):
    def __init__(self, file_name, file_type, **keywords):
        self.file_name = file_name
        self.content = {}

    def create_sheet(self, name):
        array = []
        self.content[name] = array
        return MySheetWriter(array)

    def close(self):
        with open(self.file_name, "w") as f:
            f.write(yaml.dump(self.content, default_flow_style=False))


IOPluginInfoChainV2(__name__).add_a_writer(
    relative_plugin_class_path="MyWriter",
    locations=["file"],
    file_types=["yaml"],
    stream_type="text",
)

if __name__ == "__main__":
    data_dict = {
        "sheet 1": [[1, 3, 4], [2, 4, 9]],
        "sheet 2": [["B", "C", "D"]],
    }

    save_data("mytest.yaml", data_dict)
