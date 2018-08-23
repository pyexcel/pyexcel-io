# -*- coding: utf-8 -*-
import os
from unittest import TestCase
from pyexcel_io._compact import OrderedDict
from pyexcel_io import save_data
import pyexcel_io.manager as manager
from pyexcel_io.readers.csvz import CSVZipBookReader
from pyexcel_io.writers.csvz import CSVZipBookWriter
from pyexcel_io.readers.tsvz import TSVZipBookReader
from pyexcel_io.writers.tsvz import TSVZipBookWriter
import zipfile
from nose.tools import raises
import sys

PY2 = sys.version_info[0] == 2


class TestCSVZ(TestCase):
    file_type = "csvz"
    writer_class = CSVZipBookWriter
    reader_class = CSVZipBookReader
    result = u"中,文,1,2,3"

    def setUp(self):
        self.file = "csvz." + self.file_type

    def test_writing(self):
        data = [[u"中", u"文", 1, 2, 3]]
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
        data = [[u"中", u"文", 1, 2, 3]]
        zipbook = self.writer_class()
        zipbook.open(self.file)
        zipbook.write({None: data})
        zipbook.close()
        zipreader = self.reader_class()
        zipreader.open(self.file)
        data = zipreader.read_all()
        self.assertEqual(list(data["pyexcel_sheet1"]), [[u"中", u"文", 1, 2, 3]])
        zipreader.close()

    def tearDown(self):
        os.unlink(self.file)


class TestTSVZ(TestCSVZ):
    file_type = "tsvz"
    writer_class = TSVZipBookWriter
    reader_class = TSVZipBookReader
    result = u"中\t文\t1\t2\t3"


def test_reading_from_memory():
    data = [[1, 2, 3]]
    io = manager.get_io("csvz")
    zipbook = CSVZipBookWriter()
    zipbook.open_stream(io)
    zipbook.write({None: data})
    zipbook.close()
    zipreader = CSVZipBookReader()
    zipreader.open_stream(io)
    data = zipreader.read_all()
    assert list(data["pyexcel_sheet1"]) == [[1, 2, 3]]


def test_reading_from_memory_tsvz():
    data = [[1, 2, 3]]
    io = manager.get_io("tsvz")
    zipbook = TSVZipBookWriter()
    zipbook.open_stream(io)
    zipbook.write({None: data})
    zipbook.close()
    zipreader = TSVZipBookReader()
    zipreader.open_stream(io)
    data = zipreader.read_all()
    assert list(data["pyexcel_sheet1"]) == [[1, 2, 3]]


class TestMultipleSheet(TestCase):
    file_name = "mybook.csvz"
    reader_class = CSVZipBookReader

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
    reader_class = TSVZipBookReader
