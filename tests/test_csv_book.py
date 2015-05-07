import os
from textwrap import dedent
from nose.tools import raises
from pyexcel_io import NamedContent, get_io
from pyexcel_io.csvbook import (
    CSVSheetReader,
    CSVFileReader,
    CSVinMemoryReader,
    CSVBook,
    CSVSheetWriter,
    CSVWriter
)


class TestReaders:
    def setUp(self):
        self.file_type = "csv"
        self.test_file = "csv_book." + self.file_type
        self.data = [
            ["1", "2", "3"],
            ["4", "5", "6"],
            ["7", "8", "9"]
        ]
        with open(self.test_file, 'w') as f:
            for row in self.data:
                f.write(",".join(row) + "\n")

    @raises(TypeError)
    def test_sheet_reader(self):
        CSVSheetReader(self.test_file)

    def test_sheet_file_reader(self):
        r = CSVFileReader(NamedContent(self.file_type, self.test_file))
        result = r.to_array()
        assert result == self.data

    def test_sheet_memory_reader(self):
        io = get_io(self.file_type)
        with open(self.test_file, 'r') as f:
            io.write(f.read())
        io.seek(0)
        r = CSVinMemoryReader(NamedContent(self.file_type, io))
        result = r.to_array()
        assert result == self.data

    def test_book_reader(self):
        b = CSVBook(self.test_file)
        sheets = b.sheets()
        assert sheets[self.test_file] == self.data
        
    def test_book_reader_from_memory_source(self):
        io = get_io(self.file_type)
        with open(self.test_file, 'r') as f:
            io.write(f.read())
        io.seek(0)
        b = CSVBook(None, io)
        sheets = b.sheets()
        assert sheets['csv'] == self.data

    def tearDown(self):
        os.unlink(self.test_file)


class TestReadMultipleSheets:
    def setUp(self):
        self.file_type = "csv"
        self.test_file_formatter = "csv_multiple__%s__%s." + self.file_type
        self.data = [
            ["1", "2", "3"],
            ["4", "5", "6"],
            ["7", "8", "9"]
        ]
        self.sheets = {
            "sheet1": self.data,
            "sheet2": self.data,
            "sheet3": self.data
        }
        index = 0
        for key, value in self.sheets.items():
            file_name = self.test_file_formatter % (key, index)
            with open(file_name, 'w') as f:
                for row in value:
                    f.write(",".join(row) + "\n")
            index = index + 1

    def test_multiple_sheet(self):
        b = CSVBook("csv_multiple.csv")
        sheets = b.sheets()
        assert sheets == self.sheets

    def tearDown(self):
        index = 0
        for key, value in self.sheets.items():
            file_name = self.test_file_formatter % (key, index)
            os.unlink(file_name)
            index = index + 1


class TestWriter:
    def setUp(self):
        self.file_type = "csv"
        self.test_file = "csv_book." + self.file_type
        self.data = [
            ["1", "2", "3"],
            ["4", "5", "6"],
            ["7", "8", "9"]
        ]
        self.result = dedent("""
           1,2,3
           4,5,6
           7,8,9
        """).strip('\n') + '\n' # have a trailing newline

    def test_sheet_writer(self):
        w = CSVSheetWriter(self.test_file, None)
        for row in self.data:
            w.write_row(row)
        w.close()
        with open(self.test_file, 'r') as f:
            content = f.read()
            assert content == self.result
    
    def test_book_writer(self):
        b = CSVWriter(self.test_file)
        w = b.create_sheet(None)
        for row in self.data:
            w.write_row(row)
        w.close()
        b.close()
        with open(self.test_file, 'r') as f:
            content = f.read()
            assert content == self.result
    
    def tearDown(self):
        os.unlink(self.test_file)
