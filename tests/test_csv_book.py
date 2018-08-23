#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from unittest import TestCase
from textwrap import dedent
from nose.tools import raises, eq_
import pyexcel_io.manager as manager
from pyexcel_io.sheet import NamedContent
from pyexcel_io.readers.csvr import (
    CSVSheetReader,
    CSVFileReader,
    CSVinMemoryReader,
)
from pyexcel_io.writers.csvw import CSVFileWriter, CSVMemoryWriter
from pyexcel_io._compact import BytesIO, PY2, StringIO


class TestReaders(TestCase):
    def setUp(self):
        self.file_type = "csv"
        self.test_file = "csv_book." + self.file_type
        self.data = [["1", "2", "3"], ["4", "5", "6"], ["7", "8", "9"]]
        self.expected_data = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        with open(self.test_file, "w") as f:
            for row in self.data:
                f.write(",".join(row) + "\n")

    @raises(NotImplementedError)
    def test_sheet_reader(self):
        sheet = CSVSheetReader(self.test_file)
        sheet.get_file_handle()

    def test_sheet_file_reader(self):
        r = CSVFileReader(NamedContent(self.file_type, self.test_file))
        result = list(r.to_array())
        self.assertEqual(result, self.expected_data)

    def test_sheet_memory_reader(self):
        io = manager.get_io(self.file_type)
        with open(self.test_file, "r") as f:
            io.write(f.read())
        io.seek(0)
        r = CSVinMemoryReader(NamedContent(self.file_type, io))
        result = list(r.to_array())
        self.assertEqual(result, self.expected_data)

    def tearDown(self):
        os.unlink(self.test_file)


class TestWriter(TestCase):
    def setUp(self):
        self.file_type = "csv"
        self.test_file = "csv_book." + self.file_type
        self.data = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        self.result = dedent(
            """
           1,2,3
           4,5,6
           7,8,9
        """
        ).strip("\n")

    def test_sheet_writer(self):
        w = CSVFileWriter(self.test_file, None)
        for row in self.data:
            w.write_row(row)
        w.close()
        with open(self.test_file, "r") as f:
            content = f.read().replace("\r", "")
            self.assertEqual(content.strip("\n"), self.result)

    def tearDown(self):
        os.unlink(self.test_file)


class TestMemoryWriter(TestCase):
    def setUp(self):
        self.file_type = "csv"
        self.test_file = "csv_book." + self.file_type
        self.data = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        self.result = dedent(
            """
           1,2,3
           4,5,6
           7,8,9
        """
        ).strip("\n")

    def test_sheet_writer_to_memory(self):
        io = manager.get_io(self.file_type)
        w = CSVMemoryWriter(io, None, single_sheet_in_book=True)
        for row in self.data:
            w.write_row(row)
        w.close()
        content = io.getvalue().replace("\r", "")
        self.assertEqual(content.strip("\n"), self.result)


class TestNonUniformCSV(TestCase):
    def setUp(self):
        self.file_type = "csv"
        self.test_file = "csv_book." + self.file_type
        self.data = [["1"], ["4", "5", "6", "", ""], ["", "7"]]
        with open(self.test_file, "w") as f:
            for row in self.data:
                f.write(",".join(row) + "\n")

    def test_sheet_file_reader(self):
        r = CSVFileReader(NamedContent(self.file_type, self.test_file))
        result = list(r.to_array())
        self.assertEqual(result, [[1], [4, 5, 6], ["", 7]])

    def tearDown(self):
        os.unlink(self.test_file)


def test_utf16_decoding():
    test_file = os.path.join("tests", "fixtures", "csv-encoding-utf16.csv")
    reader = CSVFileReader(NamedContent("csv", test_file), encoding="utf-16")
    content = list(reader.to_array())
    if PY2:
        content[0] = [s.encode("utf-8") for s in content[0]]
    expected = [["Äkkilähdöt", "Matkakirjoituksia", "Matkatoimistot"]]
    eq_(content, expected)


def test_utf16_encoding():
    content = [[u"Äkkilähdöt", u"Matkakirjoituksia", u"Matkatoimistot"]]
    test_file = "test-utf16-encoding.csv"
    writer = CSVFileWriter(
        test_file, None, encoding="utf-16", lineterminator="\n"
    )
    writer.write_array(content)
    writer.close()
    with open(test_file, "rb") as f:
        actual = f.read().decode("utf-16")
        if PY2:
            actual = actual.encode("utf-8")
        eq_(actual, "Äkkilähdöt,Matkakirjoituksia,Matkatoimistot\n")
    os.unlink(test_file)


def test_utf16_memory_decoding():
    test_content = u"Äkkilähdöt,Matkakirjoituksia,Matkatoimistot"
    test_content = BytesIO(test_content.encode("utf-16"))
    reader = CSVinMemoryReader(
        NamedContent("csv", test_content), encoding="utf-16"
    )
    content = list(reader.to_array())
    if PY2:
        content[0] = [s.encode("utf-8") for s in content[0]]
    expected = [["Äkkilähdöt", "Matkakirjoituksia", "Matkatoimistot"]]
    eq_(content, expected)


def test_utf16_memory_encoding():
    content = [[u"Äkkilähdöt", u"Matkakirjoituksia", u"Matkatoimistot"]]
    io = StringIO()
    writer = CSVMemoryWriter(
        io,
        None,
        lineterminator="\n",
        single_sheet_in_book=True,
        encoding="utf-16",
    )
    writer.write_array(content)
    actual = io.getvalue()
    if PY2:
        actual = actual.decode("utf-16")
    eq_(actual, u"Äkkilähdöt,Matkakirjoituksia,Matkatoimistot\n")
