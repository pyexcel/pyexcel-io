import os
from nose.tools import eq_
from pyexcel_io import get_data, save_data


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
    written_data = get_data(test_file)
    eq_(data, written_data[test_file])
    os.unlink(test_file)


def test_issue_20():
    test_file = os.path.join("tests",
                             "fixtures",
                             "issue20.csv")
    data = get_data(test_file)
    expected = [[u'to', u'infinity', u'and', u'beyond']]
    eq_(data['issue20.csv'], expected)


def test_issue_23():
    test_file = os.path.join("tests",
                             "fixtures",
                             "issue23.csv")
    data = get_data(test_file)
    expected = [
        [8204235414504252L, u'inf'],
        [82042354145042521L, u'-inf'],
        [820423541450425216L, 0],
        [820423541450425247L, 1],
        [8204235414504252490L, 1.1]
    ]
    eq_(data['issue23.csv'], expected)
