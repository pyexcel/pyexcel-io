# -*- coding: utf-8 -*-
import os
import zipfile
from unittest import TestCase

import pyexcel_io.manager as manager
from pyexcel_io import save_data
from pyexcel_io.reader import Reader
from pyexcel_io.writer import Writer
from pyexcel_io._compact import OrderedDict

from nose.tools import raises


class TestCSVZ(TestCase):
    file_type = "csvz"
    result = "中,文,1,2,3"

    def writer_class(self):
        return Writer(self.file_type)

    def reader_class(self):
        return Reader(self.file_type)

    def setUp(self):
        self.file = "csvz." + self.file_type

    def test_writing(self):
        data = [["中", "文", 1, 2, 3]]
        file_name = "pyexcel_sheet1." + self.file_type[0:3]
        zipbook = self.writer_class()
        zipbook.open(self.file)
        zipbook.write({None: data})
        zipbook.close()
        zip = zipfile.ZipFile(self.file, "r")
        self.assertEqual(zip.namelist(), [file_name])
        content = zip.read(file_name)
        content = content.decode("utf-8")
        self.assertEqual(content.replace("\r", "").strip("\n"), self.result)
        zip.close()

    def test_reading(self):
        data = [["中", "文", 1, 2, 3]]
        zipbook = self.writer_class()
        zipbook.open(self.file)
        zipbook.write({None: data})
        zipbook.close()
        zipreader = self.reader_class()
        zipreader.open(self.file)
        data = zipreader.read_all()
        self.assertEqual(list(data["pyexcel_sheet1"]), [["中", "文", 1, 2, 3]])
        zipreader.close()

    def test_reading_utf32(self):
        zip = zipfile.ZipFile(self.file, "w")
        zip.writestr("something.ext", self.result.encode("utf-32"))
        zip.close()
        zipreader = self.reader_class()
        zipreader.open(self.file)
        data = zipreader.read_all()
        self.assertEqual(list(data["something"]), [["中", "文", 1, 2, 3]])
        zipreader.close()

    def tearDown(self):
        os.unlink(self.file)


class TestTSVZ(TestCSVZ):
    file_type = "tsvz"
    result = "中\t文\t1\t2\t3"


def test_reading_from_memory():
    data = [[1, 2, 3]]
    io = manager.get_io("csvz")
    zipbook = Writer("csvz")
    zipbook.open_stream(io)
    zipbook.write({None: data})
    zipbook.close()
    zipreader = Reader("csvz")
    zipreader.open_stream(io)
    data = zipreader.read_all()
    assert list(data["pyexcel_sheet1"]) == [[1, 2, 3]]


def test_reading_from_memory_tsvz():
    data = [[1, 2, 3]]
    io = manager.get_io("tsvz")
    zipbook = Writer("tsvz")
    zipbook.open_stream(io)
    zipbook.write({None: data})
    zipbook.close()
    zipreader = Reader("tsvz")
    zipreader.open_stream(io)
    data = zipreader.read_all()
    assert list(data["pyexcel_sheet1"]) == [[1, 2, 3]]


class TestMultipleSheet(TestCase):
    file_name = "mybook.csvz"

    def reader_class(self):
        return Reader("csvz")

    def setUp(self):
        self.content = OrderedDict()
        self.content.update(
            {"Sheet 1": [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0], [7.0, 8.0, 9.0]]}
        )
        self.content.update(
            {"Sheet 2": [["X", "Y", "Z"], [1.0, 2.0, 3.0], [4.0, 5.0, 6.0]]}
        )
        self.content.update(
            {"Sheet 3": [["O", "P", "Q"], [3.0, 2.0, 1.0], [4.0, 3.0, 2.0]]}
        )
        save_data(self.file_name, self.content)

    def test_read_one_from_many_by_name(self):
        reader = self.reader_class()
        reader.open(self.file_name)
        sheets = reader.read_sheet_by_name("Sheet 1")
        self.assertEqual(
            list(sheets["Sheet 1"]), [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        )

    @raises(ValueError)
    def test_read_one_from_many_by_unknown_name(self):
        reader = self.reader_class()
        reader.open(self.file_name)
        reader.read_sheet_by_name("Sheet X")

    def test_read_one_from_many_by_index(self):
        reader = self.reader_class()
        reader.open(self.file_name)
        sheets = reader.read_sheet_by_index(0)
        self.assertEqual(
            list(sheets["Sheet 1"]), [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        )

    @raises(IndexError)
    def test_read_one_from_many_by_unknown_index(self):
        reader = self.reader_class()
        reader.open(self.file_name)
        reader.read_sheet_by_index(9999)

    def tearDown(self):
        os.unlink(self.file_name)


class TestMultipleTSVSheet(TestMultipleSheet):
    file_name = "mybook.tsvz"

    def reader_class(self):
        return Reader("tsvz")
