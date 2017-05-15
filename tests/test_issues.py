#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from nose.tools import eq_
from pyexcel_io import get_data, save_data
from pyexcel_io._compact import PY26


def test_issue_8():
    test_file = "test_issue_8.csv"
    data = [
        [1, 2],
        [],
        [],
        [],
        [3, 4]
    ]
    save_data(test_file, data)
    written_data = get_data(test_file, skip_empty_rows=False)
    eq_(data, written_data[test_file])
    os.unlink(test_file)


def test_issue_20():
    test_file = get_fixture("issue20.csv")
    data = get_data(test_file)
    expected = [[u'to', u'infinity', u'and', u'beyond']]
    eq_(data['issue20.csv'], expected)


def test_issue_23():
    test_file = get_fixture("issue23.csv")
    data = get_data(test_file)
    expected = [
        [8204235414504252, u'inf'],
        [82042354145042521, u'-inf'],
        [820423541450425216, 0],
        [820423541450425247, 1],
        [8204235414504252490, 1.1]
    ]
    eq_(data['issue23.csv'], expected)


def test_issue_28():
    from pyexcel_io.manager import pre_register, UpgradePlugin
    expected = "Please upgrade the plugin '%s' according to "
    expected += "plugin compactibility table."
    try:
        pre_register('pyexcel_test', 'test')
    except UpgradePlugin as e:
        eq_(str(e), expected % 'test')


def test_issue_33_34():
    if PY26:
        pass
    else:
        import mmap
        test_file = get_fixture("issue20.csv")
        with open(test_file, 'r+b') as f:
            memory_mapped_file = mmap.mmap(
                f.fileno(), 0, access=mmap.ACCESS_READ)
            data = get_data(memory_mapped_file, file_type='csv')
            expected = [[u'to', u'infinity', u'and', u'beyond']]
            eq_(data['csv'], expected)


def test_issue_30_utf8_BOM_header():
    content = [[u'人有悲歡離合', u'月有陰晴圓缺']]
    test_file = "test-utf8-BOM.csv"
    save_data(test_file, content, encoding="utf-8-sig", lineterminator="\n")
    custom_encoded_content = get_data(test_file, encoding="utf-8-sig")
    assert custom_encoded_content[test_file] == content
    with open(test_file, "rb") as f:
        content = f.read()
        assert content[0:3] == b'\xef\xbb\xbf'
    os.unlink(test_file)


def get_fixture(file_name):
    return os.path.join("tests", "fixtures", file_name)
