import os
from textwrap import dedent
from nose.tools import raises
from pyexcel_io import get_io, OrderedDict
from pyexcel_io.csvbook import (
    CSVBookReader,
    CSVBookWriterNew,
    TSVBookReader
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

    def test_book_reader(self):
        b = CSVBookReader()
        b.open(self.test_file)
        sheets = b.read_all()
        assert list(sheets[self.test_file]) == self.data

    def test_book_reader_from_memory_source(self):
        io = get_io(self.file_type)
        with open(self.test_file, 'r') as f:
            io.write(f.read())
        io.seek(0)
        b = CSVBookReader()
        b.open_stream(io)
        sheets = b.read_all()
        assert list(sheets['csv']) == self.data

    def tearDown(self):
        os.unlink(self.test_file)


class TestTSVReaders:
    def setUp(self):
        self.file_type = "tsv"
        self.test_file = "tsv_book." + self.file_type
        self.data = [
            ["1", "2", "3"],
            ["4", "5", "6"],
            ["7", "8", "9"]
        ]
        with open(self.test_file, 'w') as f:
            for row in self.data:
                f.write("\t".join(row) + "\n")

    def test_book_reader(self):
        b = TSVBookReader()
        b.open(self.test_file)
        sheets = b.read_all()
        assert list(sheets[self.test_file]) == self.data

    def test_book_reader_from_memory_source(self):
        io = get_io(self.file_type)
        with open(self.test_file, 'r') as f:
            io.write(f.read())
        io.seek(0)
        b = TSVBookReader()
        b.open_stream(io)
        sheets = b.read_all()
        assert list(sheets['tsv']) == self.data

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
        b = CSVBookReader()
        b.open("csv_multiple.csv")
        sheets = b.read_all()
        for key in sheets:
            sheets[key] = list(sheets[key])
        assert sheets == self.sheets

    def test_read_one_from_many_by_name(self):
        b = CSVBookReader()
        b.open("csv_multiple.csv")
        sheets = b.read_sheet_by_name("sheet1")
        assert list(sheets["sheet1"]) == self.sheets["sheet1"]

    @raises(ValueError)
    def test_read_one_from_many_by_non_existent_name(self):
        b = CSVBookReader()
        b.open("csv_multiple.csv")
        b.read_sheet_by_name("notknown")

    def test_read_one_from_many_by_index(self):
        b = CSVBookReader()
        b.open("csv_multiple.csv")
        sheets = b.read_sheet_by_index(1)
        assert list(sheets["sheet2"]) == self.sheets["sheet2"]

    @raises(IndexError)
    def test_read_one_from_many_by_wrong_index(self):
        b = CSVBookReader()
        b.open("csv_multiple.csv")
        b.read_sheet_by_index(90)

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
        w = CSVBookWriterNew()
        w.open("csv_multiple.csv")
        w.write(self.sheets)
        w.close()
        index = 0
        for key, value in self.sheets.items():
            file_name = self.test_file_formatter % (key, index)
            with open(file_name, 'r') as f:
                content = f.read().replace('\r', '')
                assert content.strip('\n') == self.result_dict[key]
            index = index + 1
        self.delete_files()

    def test_multiple_sheet_into_memory(self):
        """Write csv book into a single stream"""
        io = get_io(self.file_type)
        w = CSVBookWriterNew()
        w.open(io, lineterminator='\n')
        w.write(self.sheets)
        w.close()
        content = io.getvalue()
        expected = dedent("""\
            ---pyexcel:sheet1---
            1,2,3
            4,5,6
            7,8,9
            ---pyexcel---
            ---pyexcel:sheet2---
            1,2,3
            4,5,6
            7,8,1000
            ---pyexcel---
            ---pyexcel:sheet3---
            1,2,3
            4,5,6888
            7,8,9
            ---pyexcel---
            """)
        assert content == expected

    def test_multiple_sheet_into_memory_2(self):
        """Write csv book into a single stream"""
        io = get_io(self.file_type)
        w = CSVBookWriterNew()
        w.open(io, lineterminator='\n')
        w.write(self.sheets)
        w.close()
        reader = CSVBookReader()
        reader.open_stream(io, lineterminator='\n')
        sheets = reader.read_all()
        for sheet in sheets:
            sheets[sheet] = list(sheets[sheet])
        assert sheets == self.sheets

    def delete_files(self):
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

    def test_book_writer(self):
        w = CSVBookWriterNew()
        w.open(self.test_file)
        w.write({None: self.data})
        w.close()
        with open(self.test_file, 'r') as f:
            content = f.read().replace('\r', '')
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

    def test_book_writer_to_memroy(self):
        io = get_io(self.file_type)
        w = CSVBookWriterNew()
        w.open(io, single_sheet_in_book=True)
        w.write({self.file_type: self.data})
        w.close()
        content = io.getvalue().replace('\r', '')
        assert content.strip('\n') == self.result
