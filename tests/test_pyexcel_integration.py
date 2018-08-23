import os
import datetime
from unittest import TestCase
from textwrap import dedent

import pyexcel as pe
from pyexcel_io._compact import text_type


class TestDateFormat(TestCase):
    def setUp(self):
        self.excel_filename = "testdateformat.csv"
        self.data = [
            [
                "01/06/2016",
                datetime.date(2014, 12, 25),
                datetime.datetime(2014, 12, 25, 11, 11, 11),
                datetime.datetime(2014, 12, 25, 11, 11, 11, 10),
            ]
        ]
        pe.save_as(dest_file_name=self.excel_filename, array=self.data)

    def test_auto_detect_float(self):
        sheet = pe.get_sheet(file_name=self.excel_filename)
        self.assertEqual(sheet.to_array(), self.data)

    def test_auto_detect_float_false(self):
        expected = [
            [
                "01/06/2016",
                "2014-12-25",
                "2014-12-25 11:11:11",
                "2014-12-25 11:11:11.000010",
            ]
        ]
        sheet = pe.get_sheet(
            file_name=self.excel_filename, auto_detect_datetime=False
        )
        self.assertEqual(sheet.to_array(), expected)

    def tearDown(self):
        os.unlink(self.excel_filename)


class TestAutoDetectInt(TestCase):
    def setUp(self):
        self.content = [[1, 2, 3.1]]
        self.test_file = "test_auto_detect_init.csv"
        pe.save_as(array=self.content, dest_file_name=self.test_file)

    def test_auto_detect_int(self):
        sheet = pe.get_sheet(file_name=self.test_file)
        expected = dedent(
            """
        test_auto_detect_init.csv:
        +---+---+-----+
        | 1 | 2 | 3.1 |
        +---+---+-----+"""
        ).strip()
        self.assertEqual(str(sheet), expected)

    def test_get_book_auto_detect_int(self):
        book = pe.get_book(file_name=self.test_file)
        expected = dedent(
            """
        test_auto_detect_init.csv:
        +---+---+-----+
        | 1 | 2 | 3.1 |
        +---+---+-----+"""
        ).strip()
        self.assertEqual(str(book), expected)

    def test_auto_detect_int_false(self):
        sheet = pe.get_sheet(file_name=self.test_file, auto_detect_int=False)
        expected = dedent(
            """
        test_auto_detect_init.csv:
        +-----+-----+-----+
        | 1.0 | 2.0 | 3.1 |
        +-----+-----+-----+"""
        ).strip()
        self.assertEqual(str(sheet), expected)

    def test_get_book_auto_detect_int_false(self):
        book = pe.get_book(file_name=self.test_file, auto_detect_int=False)
        expected = dedent(
            """
        test_auto_detect_init.csv:
        +-----+-----+-----+
        | 1.0 | 2.0 | 3.1 |
        +-----+-----+-----+"""
        ).strip()
        self.assertEqual(str(book), expected)

    def tearDown(self):
        os.unlink(self.test_file)


class TestAutoDetectFloat(TestCase):
    """
    csv format would keep all as text 1, 2.0, 3.1
    without auto-detection, they all stay as text format after reading
    out
    """

    def setUp(self):
        self.content = [[1, 2.0, 3.1]]
        self.test_file = "test_auto_detect_init.csv"
        pe.save_as(array=self.content, dest_file_name=self.test_file)

    def test_auto_detect_float_false(self):
        sheet = pe.get_sheet(file_name=self.test_file, auto_detect_float=False)
        self.assertEqual(sheet.to_array(), [[1, "2.0", "3.1"]])
        expected = dedent(
            """
        test_auto_detect_init.csv:
        +---+-----+-----+
        | 1 | 2.0 | 3.1 |
        +---+-----+-----+"""
        ).strip()
        self.assertEqual(str(sheet), expected)

    def test_get_book_auto_detect_float_false(self):
        book = pe.get_book(file_name=self.test_file, auto_detect_float=False)
        self.assertEqual(book[0].to_array(), [[1, "2.0", "3.1"]])
        expected = dedent(
            """
        test_auto_detect_init.csv:
        +---+-----+-----+
        | 1 | 2.0 | 3.1 |
        +---+-----+-----+"""
        ).strip()
        self.assertEqual(str(book), expected)

    def tearDown(self):
        os.unlink(self.test_file)


class TestSpecialStrings(TestCase):
    """
    csv format would keep all as text 1, 2.0, 3.1
    without auto-detection, they all stay as text format after reading
    out
    """

    def setUp(self):
        self.content = [["01", 1, 2.0, 3.1, "NaN", "nan"]]
        self.test_file = "test_auto_detect_init.csv"
        pe.save_as(array=self.content, dest_file_name=self.test_file)

    def test_auto_detect_float_true(self):
        sheet = pe.get_sheet(file_name=self.test_file)
        self.assertEqual(sheet.to_array(), [["01", 1, 2, 3.1, "NaN", "nan"]])

    def test_auto_detect_float_false(self):
        sheet = pe.get_sheet(file_name=self.test_file, auto_detect_float=False)
        self.assertEqual(
            sheet.to_array(), [["01", 1, "2.0", "3.1", "NaN", "nan"]]
        )

    def test_auto_detect_float_ignore_nan_text(self):
        sheet = pe.get_sheet(file_name=self.test_file, ignore_nan_text=True)
        self.assertEqual(sheet.to_array(), [["01", 1, 2.0, 3.1, "NaN", "nan"]])

    def test_auto_detect_float_default_float_nan(self):
        sheet = pe.get_sheet(file_name=self.test_file, default_float_nan="nan")
        result = sheet.to_array()
        assert isinstance(result[0][5], float)
        assert isinstance(result[0][4], text_type)

    def tearDown(self):
        os.unlink(self.test_file)
