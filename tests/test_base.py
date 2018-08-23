from pyexcel_io.sheet import SheetReader, SheetWriter, NamedContent
from pyexcel_io.book import BookWriter
from pyexcel_io.utils import is_empty_array
from nose.tools import raises


@raises(NotImplementedError)
def test_book_writer():
    book = BookWriter()
    book.create_sheet("test")


def test_is_empty_array():
    a = ["", "", "", ""]
    assert is_empty_array(a) is True
    b = [1, "", "", ""]
    assert is_empty_array(b) is False


class ArrayWriter(SheetWriter):
    def set_sheet_name(self, name):
        self._native_sheet.name = name

    def write_row(self, array):
        self._native_sheet.payload.append(array)


class TestSheetReader:
    @raises(Exception)
    def test_abstractness(self):
        reader = SheetReader("test")
        reader.cell_value(1, 2)

    @raises(Exception)
    def test_number_of_columns(self):
        reader = SheetReader("test")
        reader.number_of_columns()

    @raises(Exception)
    def test_number_of_rows(self):
        reader = SheetReader("test")
        reader.number_of_rows()

    def test_to_array(self):
        name = "test"

        class B(SheetReader):
            @property
            def name(self):
                return self._native_sheet

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

        d = D("t", "e", "s")
        d.write_row([11, 11])

    def test_writer(self):
        native_sheet = NamedContent("test", [])
        content = [[1, 2], [3, 4], [5, 6]]
        writer = ArrayWriter(None, native_sheet, "test")
        writer.write_row(content[0])
        writer.write_array(content[1:])
        assert native_sheet.payload == content

    def test_writer2(self):
        native_sheet = NamedContent("test", [])
        content = [[1, 2], [3, 4], [5, 6]]
        writer = ArrayWriter(None, native_sheet, None)
        writer.write_row(content[0])
        writer.write_array(content[1:])
        assert native_sheet.payload == content
        assert native_sheet.name == "pyexcel_sheet1"
