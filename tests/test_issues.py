#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from nose import SkipTest
from nose.tools import eq_
from pyexcel_io import get_data, save_data
from pyexcel_io._compact import PY26
import pyexcel as p

IN_TRAVIS = "TRAVIS" in os.environ


def test_issue_8():
    test_file = "test_issue_8.csv"
    data = [[1, 2], [], [], [], [3, 4]]
    save_data(test_file, data)
    written_data = get_data(test_file, skip_empty_rows=False)
    eq_(data, written_data[test_file])
    os.unlink(test_file)


def test_issue_20():
    test_file = get_fixture("issue20.csv")
    data = get_data(test_file)
    expected = [[u"to", u"infinity", u"and", u"beyond"]]
    eq_(data["issue20.csv"], expected)


def test_issue_23():
    test_file = get_fixture("issue23.csv")
    data = get_data(test_file)
    expected = [
        [8204235414504252, u"inf"],
        [82042354145042521, u"-inf"],
        [820423541450425216, 0],
        [820423541450425247, 1],
        [8204235414504252490, 1.1],
    ]
    eq_(data["issue23.csv"], expected)


# def test_issue_28():
#     from pyexcel_io.plugins import readers
#     from pyexcel_io.exceptions import UpgradePlugin
#     expected = "Please upgrade the plugin '%s' according to "
#     expected += "plugin compactibility table."
#     try:
#         readers.load_me_later('pyexcel_test')
#     except UpgradePlugin as e:
#         eq_(str(e), expected % 'pyexcel_test')


def test_issue_33_34():
    if PY26:
        pass
    else:
        import mmap

        test_file = get_fixture("issue20.csv")
        with open(test_file, "r+b") as f:
            memory_mapped_file = mmap.mmap(
                f.fileno(), 0, access=mmap.ACCESS_READ
            )
            data = get_data(memory_mapped_file, file_type="csv")
            expected = [[u"to", u"infinity", u"and", u"beyond"]]
            eq_(data["csv"], expected)


def test_issue_30_utf8_BOM_header():
    content = [[u"人有悲歡離合", u"月有陰晴圓缺"]]
    test_file = "test-utf8-BOM.csv"
    save_data(test_file, content, encoding="utf-8-sig", lineterminator="\n")
    custom_encoded_content = get_data(test_file, encoding="utf-8-sig")
    assert custom_encoded_content[test_file] == content
    with open(test_file, "rb") as f:
        content = f.read()
        assert content[0:3] == b"\xef\xbb\xbf"
    os.unlink(test_file)


def test_issue_33_34_utf32_encoded_file():
    if PY26:
        pass
    else:
        check_mmap_encoding("utf-32")


def test_issue_33_34_utf32be_encoded_file():
    if PY26:
        pass
    else:
        check_mmap_encoding("utf-32-be")


def test_issue_33_34_utf32le_encoded_file():
    if PY26:
        pass
    else:
        check_mmap_encoding("utf-32-le")


def test_issue_33_34_utf16_encoded_file():
    if PY26:
        pass
    else:
        check_mmap_encoding("utf-16")


def test_issue_33_34_utf16be_encoded_file():
    if PY26:
        pass
    else:
        check_mmap_encoding("utf-16-be")


def test_issue_33_34_utf16le_encoded_file():
    if PY26:
        pass
    else:
        check_mmap_encoding("utf-16-le")


def test_issue_33_34_utf8_encoded_file():
    if PY26:
        pass
    else:
        check_mmap_encoding("utf-8")


def check_mmap_encoding(encoding):
    import mmap

    content = [
        [u"Äkkilähdöt", u"Matkakirjoituksia", u"Matkatoimistot"],
        [u"Äkkilähdöt", u"Matkakirjoituksia", u"Matkatoimistot"],
    ]
    test_file = "test-%s-encoding-in-mmap-file.csv" % encoding
    save_data(test_file, content, encoding=encoding)
    with open(test_file, "r+b") as f:
        memory_mapped_file = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
        data = get_data(memory_mapped_file, file_type="csv", encoding=encoding)
        eq_(data["csv"], content)

    os.unlink(test_file)


def test_issue_35_encoding_for_file_content():
    encoding = "utf-16"
    content = [
        [u"Äkkilähdöt", u"Matkakirjoituksia", u"Matkatoimistot"],
        [u"Äkkilähdöt", u"Matkakirjoituksia", u"Matkatoimistot"],
    ]
    test_file = "test-%s-encoding-in-mmap-file.csv" % encoding
    save_data(test_file, content, encoding=encoding)
    with open(test_file, "r+b") as f:
        csv_content = f.read()
        data = get_data(csv_content, file_type="csv", encoding=encoding)
        eq_(data["csv"], content)

    os.unlink(test_file)


def test_issue_43():
    # if not IN_TRAVIS:
    #    raise SkipTest()
    p.get_book(
        url="https://github.com/pyexcel/pyexcel-xls/raw/master/tests/fixtures/file_with_an_empty_sheet.xls"
    )
    # flake8: noqa


def test_pyexcel_issue_138():
    array = [["123_122", "123_1.", "123_1.0"]]
    save_data("test.csv", array)
    data = get_data("test.csv")
    expected = [["123_122", "123_1.", "123_1.0"]]
    eq_(data["test.csv"], expected)
    os.unlink("test.csv")


def get_fixture(file_name):
    return os.path.join("tests", "fixtures", file_name)
