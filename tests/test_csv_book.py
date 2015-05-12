import os
from textwrap import dedent
from nose.tools import raises
from pyexcel_io import NamedContent, get_io, OrderedDict
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
        self.sheets = OrderedDict()
        self.sheets.update({"sheet1": self.data})
        self.sheets.update({"sheet2": self.data})
        self.sheets.update({"sheet3": self.data})
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


class TestWriteMultipleSheets:
    def setUp(self):
        self.file_type = "csv"
        self.test_file_formatter = "csv_multiple__%s__%s." + self.file_type
        self.data1 = [
            ["1", "2", "3"],
            ["4", "5", "6"],
            ["7", "8", "9"]
        ]
        self.data2 = [
            ["1", "2", "3"],
            ["4", "5", "6"],
            ["7", "8", "1000"]
        ]
        self.data3 = [
            ["1", "2", "3"],
            ["4", "5", "6888"],
            ["7", "8", "9"]
        ]
        self.sheets = OrderedDict()
        self.sheets.update({"sheet1": self.data1})
        self.sheets.update({"sheet2": self.data2})
        self.sheets.update({"sheet3": self.data3})
        self.result_dict = OrderedDict()        
        self.result1 = dedent("""
           1,2,3
           4,5,6
           7,8,9
        """).strip('\n')
        self.result2 = dedent("""
           1,2,3
           4,5,6
           7,8,1000
        """).strip('\n')
        self.result3 = dedent("""
           1,2,3
           4,5,6888
           7,8,9
        """).strip('\n')
        self.result_dict.update({"sheet1": self.result1})
        self.result_dict.update({"sheet2": self.result2})
        self.result_dict.update({"sheet3": self.result3})

    def test_multiple_sheet(self):
        """Write csv book into multiple file"""
        b = CSVWriter("csv_multiple.csv")
        for key, value in self.sheets.items():
            w = b.create_sheet(key)
            w.write_array(value)
            w.close()
        b.close()
        index = 0
        for key, value in self.sheets.items():
            file_name = self.test_file_formatter % (key, index)
            with open(file_name, 'r') as f:
                content = f.read().replace('\r', '')
                assert content.strip('\n') == self.result_dict[key]
            index = index + 1

    #def test_multiple_sheet_into_memory(self):
    #    """Write csv book into a single stream"""
    #    io = get_io(self.file_type)
    #    b = CSVWriter(io)
    #    for key, value in self.sheets.items():
    #        w = b.create_sheet(key)
    #        w.write_array(value)
    #        w.close()
    #    b.close()
    #    content = io.getvalue()    
    #    index = 0
    #    for key, value in self.content.split('---pyexcel---\r\n'):
    #        file_name = self.test_file_formatter % (key, index)
    #        with open(file_name, 'r') as f:
    #            content = f.read().replace('\r', '')
    #            assert content.strip('\n') == self.result_dict[key]
    #        index = index + 1

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
        """).strip('\n')

    def test_sheet_writer(self):
        w = CSVSheetWriter(self.test_file, None)
        for row in self.data:
            w.write_row(row)
        w.close()
        with open(self.test_file, 'r') as f:
            content = f.read().replace('\r', '')
            assert content.strip('\n') == self.result
    
    def test_book_writer(self):
        b = CSVWriter(self.test_file)
        w = b.create_sheet(None)
        for row in self.data:
            w.write_row(row)
        w.close()
        b.close()
        with open(self.test_file, 'r') as f:
            content = f.read().replace('\r', '')
            print content.strip('\n').split('\n')
            print self.result.split('\n')
            assert content.strip('\n') == self.result
    
    def tearDown(self):
        os.unlink(self.test_file)


class TestMemoryWriter:
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
        """).strip('\n')

    def test_sheet_writer_to_memory(self):
        io = get_io(self.file_type)
        w = CSVSheetWriter(io, None, single_sheet_in_book=True)
        for row in self.data:
            w.write_row(row)
        w.close()
        content = io.getvalue().replace('\r', '')
        assert content.strip('\n') == self.result
    
    def test_book_writer_to_memroy(self):
        io = get_io(self.file_type)
        b = CSVWriter(io, single_sheet_in_book=True)
        w = b.create_sheet(None)
        for row in self.data:
            w.write_row(row)
        w.close()
        b.close()
        content = io.getvalue().replace('\r', '')
        assert content.strip('\n') == self.result
