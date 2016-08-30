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
    test_file= os.path.join("tests",
                            "fixtures",
                            "issue8.csv")
    data = get_data(test_file)
    expected = [[u'to', u'infinity', u'and', u'beyond']]
    eq_(data['issue8.csv'], expected)