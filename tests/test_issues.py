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


def get_fixture(file_name):
    return os.path.join("tests", "fixtures", file_name)
