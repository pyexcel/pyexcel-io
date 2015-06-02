from pyexcel_io import (
    SheetReaderBase, SheetReader, BookReader,
    SheetWriter, BookWriter, NamedContent,
    BookReaderBase, SheetWriterBase,
)
from pyexcel_io.base import is_empty_array
from nose.tools import raises


def test_is_empty_array():
    a=["", "", "", ""]
    assert is_empty_array(a) == True
    b=[1, "", "", ""]
    assert is_empty_array(b) == False


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


class DictReader(BookReader):
    def sheet_iterator(self):
        BookReader.sheet_iterator(self)
        return [NamedContent(name, self.native_book[name]) for name in self.native_book]

    def get_sheet(self, native_sheet):
        BookReader.get_sheet(self, native_sheet)
        return ArrayReader(native_sheet)

    def load_from_file(self, file_content):
        BookReader.load_from_file(self, file_content)
        return file_content # just pass it

    def load_from_memory(self, file_name):
        BookReader.load_from_memory(self, file_name)
        return file_name # just pass it


class ArrayWriter(SheetWriter):
    def set_sheet_name(self, name):
        self.native_sheet.name = name

    def write_row(self, array):
        self.native_sheet.payload.append(array)


class DictWriter(BookWriter):
    def __init__(self, file):
        BookWriter.__init__(self, file)
        self.dict = {}
        
    def create_sheet(self, name):
        new_array = []
        self.dict[name] = new_array
        return ArrayWriter(self.dict, NamedContent(name, new_array), name)

    def close(self):
        BookWriter.close(self)


class TestSheetReaderBase:

    @raises(TypeError)
    def test_abstractness(self):
        SheetReaderBase("test")

    def test_to_array(self):
        name = "test"
        class B(SheetReaderBase):
            @property
            def name(self):
                return self.native_sheet
            def to_array(self):
                SheetReaderBase.to_array(self)
        B(name).to_array()
        assert B(name).name == name


class TestSheetReader:
    
    @raises(TypeError)
    def test_abstractness(self):
        SheetReader("test")

    def test_abstract_functions(self):
        content = [
            [1,2,3],
            [4,5,6]
        ]
        areader = ArrayReader(NamedContent("Test", content))
        expected = areader.to_array()
        assert content == expected


class TestBookReaderBase:
    @raises(TypeError)
    def test_abstractness(self):
        BookReaderBase()

    def test_sheets(self):
        sample = {"a": 1}
        class C(BookReaderBase):
            def sheets(self):
                BookReaderBase.sheets(self)
                return sample

        assert C().sheets() == sample


class TestBookReader:
    def setUp(self):
        self.content = {
            "Sheet 1": [
                [1,2,3],
                [4,5,6]
            ],
            "Sheet 2": [
                ['a', 'b', 'c']
            ]
        }

    @raises(TypeError)
    def test_abstractness(self):
        BookReader("testfile")

    def test_load_from_file(self):
        reader = DictReader(self.content)
        assert self.content == reader.sheets()
        
    def test_load_from_memory(self):
        reader = DictReader(None, self.content)
        assert self.content == reader.sheets()      

class TestSheetWriterBase:
    @raises(TypeError)
    def test_abstractness(self):
        SheetWriterBase("test")

    def test_sheet_writer_base(self):
        class D(SheetWriterBase):
            def close(self):
                SheetWriterBase.close(self)
                pass

            def set_size(self, size):
                SheetWriterBase.set_size(self, size)
                pass

            def write_array(self, table):
                SheetWriterBase.write_array(self, table)
                pass

        d = D()
        d.set_size(10)
        d.write_array([11,11])
        d.close()            
        
class TestSheetWriter:
    @raises(TypeError)
    def test_abstractness(self):
        SheetWriter("te","st", "abstract")

    def test_inheritance(self):
        class D(SheetWriter):
            def write_row(self, row):
                SheetWriter.write_row(self, row)
                pass

        d = D('t','e','s')
        d.write_row([11,11])
        d.set_size(10)

    def test_writer(self):
        native_sheet = NamedContent("test", [])
        content = [
            [1,2],
            [3,4],
            [5,6]
        ]
        writer = ArrayWriter(None, native_sheet, "test")
        writer.write_row(content[0])
        writer.write_array(content[1:])
        assert native_sheet.payload == content

    def test_writer2(self):
        native_sheet = NamedContent("test", [])
        content = [
            [1,2],
            [3,4],
            [5,6]
        ]
        writer = ArrayWriter(None, native_sheet, None)
        writer.write_row(content[0])
        writer.write_array(content[1:])
        assert native_sheet.payload == content
        assert native_sheet.name == "pyexcel_sheet1"


class TestBookWriter:
    @raises(TypeError)
    def test_book_writer_abstractness(self):
        BookWriter("te")

    def test_inheritance(self):
        class E(BookWriter):
            def create_sheet(self, name):
                BookWriter.create_sheet(self, name)
                pass

            def close(self):
                BookWriter.close(self)
                pass

        E("test").create_sheet("test")
        E("test").close()

    def test_book_writer(self):
        content = {
            "Sheet1": [[1,2],[3,4]],
            "Sheet2": [['a', 'b']]
        }

        writer = DictWriter("afile")
        writer.write(content)
        writer.close()
        assert writer.dict == content
