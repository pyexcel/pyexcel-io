from pyexcel_io.sheet import (
    SheetReader,
    SheetWriter, NamedContent
)
from pyexcel_io.utils import is_empty_array
from nose.tools import raises


def test_is_empty_array():
    a = ["", "", "", ""]
    assert is_empty_array(a) is True
    b = [1, "", "", ""]
    assert is_empty_array(b) is False


class ArrayReader(SheetReader):
    @property
    def name(self):
        SheetReader.name
        return self.native_sheet.name

    def number_of_columns(self):
        SheetReader.number_of_columns(self)
        return len(self.native_sheet.payload[0])

    def number_of_rows(self):
        SheetReader.number_of_rows(self)
        return len(self.native_sheet.payload)

    def cell_value(self, row, column):
        SheetReader.cell_value(self, row, column)
        return self.native_sheet.payload[row][column]


class ArrayWriter(SheetWriter):
    def set_sheet_name(self, name):
        self.native_sheet.name = name

    def write_row(self, array):
        self.native_sheet.payload.append(array)


class TestSheetReader:

    @raises(NotImplementedError)
    def test_abstractness(self):
        reader = SheetReader("test")
        reader._cell_value(1, 2)

    def test_to_array(self):
        name = "test"

        class B(SheetReader):
            @property
            def name(self):
                return self.native_sheet

            def to_array(self):
                pass
        b = B(name)
        b.to_array()
        assert b.name == name


class TestSheetWriter:

    @raises(NotImplementedError)
    def test_abstractness(self):
        writer = SheetWriter("te", "st", "abstract")
        writer.write_row([])

    def test_inheritance(self):
        class D(SheetWriter):
            def write_row(self, row):
                pass

        d = D('t', 'e', 's')
        d.write_row([11, 11])
        d.set_size(10)

    def test_writer(self):
        native_sheet = NamedContent("test", [])
        content = [
            [1, 2],
            [3, 4],
            [5, 6]
        ]
        writer = ArrayWriter(None, native_sheet, "test")
        writer.write_row(content[0])
        writer.write_array(content[1:])
        assert native_sheet.payload == content

    def test_writer2(self):
        native_sheet = NamedContent("test", [])
        content = [
            [1, 2],
            [3, 4],
            [5, 6]
        ]
        writer = ArrayWriter(None, native_sheet, None)
        writer.write_row(content[0])
        writer.write_array(content[1:])
        assert native_sheet.payload == content
        assert native_sheet.name == "pyexcel_sheet1"
