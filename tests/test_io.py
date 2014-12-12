from pyexcel_io import (
    SheetReaderBase, SheetReader, BookReader,
    SheetWriter, BookWriter, NamedContent
)
from nose.tools import raises


#class NamedArray:
#    def __init__(self, name, array):
#        self.name = name
#        self.array = array


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
    def sheetIterator(self):
        BookReader.sheetIterator(self)
        return [NamedContent(name, self.native_book[name]) for name in self.native_book]

    def getSheet(self, native_sheet):
        BookReader.getSheet(self, native_sheet)
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


class AbstractnessBase:
    """Test all abstract class that cannot be instantiated
    """
    @raises(TypeError)
    def test(self):
        self.testclass()


class TestSheetReaderBase(AbstractnessBase):
    def setUp(self):
        self.testclass = SheetReaderBase

    def test_to_array(self):
        class B(SheetReaderBase):
            def to_array(self):
                SheetReaderBase.to_array(self)
        B("test").to_array()


class TestSheetReader(AbstractnessBase):
    def setUp(self):
        self.testclass = SheetReader

    def test_abstract_functions(self):
        content = [
            [1,2,3],
            [4,5,6]
        ]
        areader = ArrayReader(NamedContent("Test", content))
        expected = areader.to_array()
        assert content == expected


class TestBookReader(AbstractnessBase):
    def setUp(self):
        self.testclass = BookReader
        self.content = {
            "Sheet 1": [
                [1,2,3],
                [4,5,6]
            ],
            "Sheet 2": [
                ['a', 'b', 'c']
            ]
        }

    def test_load_from_file(self):
        reader = DictReader(self.content)
        assert self.content == reader.sheets()
        
    def test_load_from_memory(self):
        reader = DictReader(None, self.content)
        assert self.content == reader.sheets()      


class TestSheetWriter(AbstractnessBase):
    def setUp(self):
        self.testclass = SheetWriter

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


class TestBookWriter(AbstractnessBase):
    def setUp(self):
        self.testclass = BookWriter

    def test_book_writer(self):
        content = {
            "Sheet1": [[1,2],[3,4]],
            "Sheet2": [['a', 'b']]
        }

        writer = DictWriter("afile")
        writer.write(content)
        writer.close()
        assert writer.dict == content