import os
from unittest import TestCase
from textwrap import dedent
from nose.tools import raises
import pyexcel_io.manager as manager
from pyexcel_io._compact import OrderedDict
from pyexcel_io.readers.csvr import CSVBookReader
from pyexcel_io.readers.tsv import TSVBookReader
from pyexcel_io.writers.csvw import CSVBookWriter
from pyexcel_io.writers.tsv import TSVBookWriter


class TestCSVReaders(TestCase):
    file_type = "csv"
    reader_class = CSVBookReader
    delimiter = ","

    def setUp(self):
        self.test_file = "csv_book." + self.file_type
        self.data = [["1", "2", "3"], ["4", "5", "6"], ["7", "8", "9"]]
        self.expected_data = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        with open(self.test_file, "w") as f:
            for row in self.data:
                f.write(self.delimiter.join(row) + "\n")

    def test_book_reader(self):
        b = self.reader_class()
        b.open(self.test_file)
        sheets = b.read_all()
        self.assertEqual(list(sheets[self.test_file]), self.expected_data)

    def test_book_reader_from_memory_source(self):
        io = manager.get_io(self.file_type)
        with open(self.test_file, "r") as f:
            io.write(f.read())
        io.seek(0)
        b = self.reader_class()
        b.open_stream(io)
        sheets = b.read_all()
        self.assertEqual(list(sheets[self.file_type]), self.expected_data)

    def tearDown(self):
        os.unlink(self.test_file)


class TestTSVReaders(TestCSVReaders):
    file_type = "tsv"
    reader_class = TSVBookReader
    delimiter = "\t"


class TestReadMultipleSheets(TestCase):
    file_type = "csv"
    reader_class = CSVBookReader
    delimiter = ","

    def setUp(self):
        self.test_file_formatter = "csv_multiple__%s__%s." + self.file_type
        self.merged_book_file = "csv_multiple." + self.file_type
        self.data = [["1", "2", "3"], ["4", "5", "6"], ["7", "8", "9"]]
        self.expected_data = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        self.sheets = OrderedDict()
        self.sheets.update({"sheet1": self.data})
        self.sheets.update({"sheet2": self.data})
        self.sheets.update({"sheet3": self.data})
        self.expected_sheets = OrderedDict()
        self.expected_sheets.update({"sheet1": self.expected_data})
        self.expected_sheets.update({"sheet2": self.expected_data})
        self.expected_sheets.update({"sheet3": self.expected_data})
        index = 0
        for key, value in self.sheets.items():
            file_name = self.test_file_formatter % (key, index)
            with open(file_name, "w") as f:
                for row in value:
                    f.write(self.delimiter.join(row) + "\n")
            index = index + 1

    def test_multiple_sheet(self):
        b = self.reader_class()
        b.open(self.merged_book_file)
        sheets = b.read_all()
        for key in sheets:
            sheets[key] = list(sheets[key])
        self.assertEqual(sheets, self.expected_sheets)

    def test_read_one_from_many_by_name(self):
        b = self.reader_class()
        b.open(self.merged_book_file)
        sheets = b.read_sheet_by_name("sheet1")
        self.assertEqual(
            list(sheets["sheet1"]), self.expected_sheets["sheet1"]
        )

    @raises(ValueError)
    def test_read_one_from_many_by_non_existent_name(self):
        b = self.reader_class()
        b.open(self.merged_book_file)
        b.read_sheet_by_name("notknown")

    def test_read_one_from_many_by_index(self):
        b = self.reader_class()
        b.open(self.merged_book_file)
        sheets = b.read_sheet_by_index(1)
        self.assertEqual(
            list(sheets["sheet2"]), self.expected_sheets["sheet2"]
        )

    @raises(IndexError)
    def test_read_one_from_many_by_wrong_index(self):
        b = self.reader_class()
        b.open(self.merged_book_file)
        b.read_sheet_by_index(90)

    def tearDown(self):
        index = 0
        for key, value in self.sheets.items():
            file_name = self.test_file_formatter % (key, index)
            os.unlink(file_name)
            index = index + 1


class TestTSVBookReaders(TestReadMultipleSheets):
    file_type = "tsv"
    reader_class = TSVBookReader
    delimiter = "\t"


class TestWriteMultipleSheets(TestCase):
    file_type = "csv"
    writer_class = CSVBookWriter
    reader_class = CSVBookReader
    result1 = dedent(
        """
        1,2,3
        4,5,6
        7,8,9
        """
    ).strip("\n")
    result2 = dedent(
        """
        1,2,3
        4,5,6
        7,8,1000
        """
    ).strip("\n")
    result3 = dedent(
        """
        1,2,3
        4,5,6888
        7,8,9
        """
    ).strip("\n")
    merged = dedent(
        """\
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
        """
    )

    def setUp(self):
        self.test_file_formatter = "csv_multiple__%s__%s." + self.file_type
        self.merged_book_file = "csv_multiple." + self.file_type
        self.data1 = [["1", "2", "3"], ["4", "5", "6"], ["7", "8", "9"]]
        self.data2 = [["1", "2", "3"], ["4", "5", "6"], ["7", "8", "1000"]]
        self.data3 = [["1", "2", "3"], ["4", "5", "6888"], ["7", "8", "9"]]
        self.expected_data1 = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        self.expected_data2 = [[1, 2, 3], [4, 5, 6], [7, 8, 1000]]
        self.expected_data3 = [[1, 2, 3], [4, 5, 6888], [7, 8, 9]]
        self.sheets = OrderedDict()
        self.sheets.update({"sheet1": self.data1})
        self.sheets.update({"sheet2": self.data2})
        self.sheets.update({"sheet3": self.data3})
        self.expected_sheets = OrderedDict()
        self.expected_sheets.update({"sheet1": self.expected_data1})
        self.expected_sheets.update({"sheet2": self.expected_data2})
        self.expected_sheets.update({"sheet3": self.expected_data3})
        self.result_dict = OrderedDict()
        self.result_dict.update({"sheet1": self.result1})
        self.result_dict.update({"sheet2": self.result2})
        self.result_dict.update({"sheet3": self.result3})

    def test_multiple_sheet(self):
        w = self.writer_class()
        w.open(self.merged_book_file)
        w.write(self.sheets)
        w.close()
        index = 0
        for key, value in self.sheets.items():
            file_name = self.test_file_formatter % (key, index)
            with open(file_name, "r") as f:
                content = f.read().replace("\r", "")
                assert content.strip("\n") == self.result_dict[key]
            index = index + 1
        self.delete_files()

    def test_multiple_sheet_into_memory(self):
        io = manager.get_io(self.file_type)
        w = self.writer_class()
        w.open(io, lineterminator="\n")
        w.write(self.sheets)
        w.close()
        content = io.getvalue()
        self.assertEqual(content, self.merged)

    def test_multiple_sheet_into_memory_2(self):
        """Write csv book into a single stream"""
        io = manager.get_io(self.file_type)
        w = self.writer_class()
        w.open(io, lineterminator="\n")
        w.write(self.sheets)
        w.close()
        reader = self.reader_class()
        reader.open_stream(io, lineterminator="\n", multiple_sheets=True)
        sheets = reader.read_all()
        for sheet in sheets:
            sheets[sheet] = list(sheets[sheet])
        self.assertEqual(sheets, self.expected_sheets)

    def delete_files(self):
        index = 0
        for key, value in self.sheets.items():
            file_name = self.test_file_formatter % (key, index)
            os.unlink(file_name)
            index = index + 1


class TestTSVWriteMultipleSheets(TestWriteMultipleSheets):
    file_type = "tsv"
    writer_class = TSVBookWriter
    reader_class = TSVBookReader
    result1 = dedent(
        """
        1\t2\t3
        4\t5\t6
        7\t8\t9
        """
    ).strip("\n")
    result2 = dedent(
        """
        1\t2\t3
        4\t5\t6
        7\t8\t1000
        """
    ).strip("\n")
    result3 = dedent(
        """
        1\t2\t3
        4\t5\t6888
        7\t8\t9
        """
    ).strip("\n")
    merged = dedent(
        """\
        ---pyexcel:sheet1---
        1\t2\t3
        4\t5\t6
        7\t8\t9
        ---pyexcel---
        ---pyexcel:sheet2---
        1\t2\t3
        4\t5\t6
        7\t8\t1000
        ---pyexcel---
        ---pyexcel:sheet3---
        1\t2\t3
        4\t5\t6888
        7\t8\t9
        ---pyexcel---
        """
    )


class TestWriter(TestCase):
    file_type = "csv"
    writer_class = CSVBookWriter
    result = dedent(
        """
        1,2,3
        4,5,6
        7,8,9
        """
    ).strip("\n")

    def setUp(self):
        self.test_file = "csv_book." + self.file_type
        self.data = [["1", "2", "3"], ["4", "5", "6"], ["7", "8", "9"]]

    def test_book_writer(self):
        w = self.writer_class()
        w.open(self.test_file)
        w.write({None: self.data})
        w.close()
        with open(self.test_file, "r") as f:
            content = f.read().replace("\r", "")
            self.assertEqual(content.strip("\n"), self.result)

    def tearDown(self):
        os.unlink(self.test_file)


class TestTSVWriters(TestWriter):
    file_type = "tsv"
    writer_class = TSVBookWriter
    result = dedent(
        """
        1\t2\t3
        4\t5\t6
        7\t8\t9
        """
    ).strip("\n")


class TestMemoryWriter(TestCase):
    file_type = "csv"
    writer_class = CSVBookWriter
    result = dedent(
        """
           1,2,3
           4,5,6
           7,8,9
        """
    ).strip("\n")

    def setUp(self):
        self.test_file = "csv_book." + self.file_type
        self.data = [["1", "2", "3"], ["4", "5", "6"], ["7", "8", "9"]]

    def test_book_writer_to_memroy(self):
        io = manager.get_io(self.file_type)
        w = self.writer_class()
        w.open(io, single_sheet_in_book=True)
        w.write({self.file_type: self.data})
        w.close()
        content = io.getvalue().replace("\r", "")
        assert content.strip("\n") == self.result


class TestTSVMemoryWriter(TestMemoryWriter):
    file_type = "tsv"
    writer_class = TSVBookWriter
    result = dedent(
        """
           1\t2\t3
           4\t5\t6
           7\t8\t9
        """
    ).strip("\n")
