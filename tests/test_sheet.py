from nose.tools import eq_
from pyexcel_io.sheet import SheetWriter


class MyWriter(SheetWriter):

    def set_size(self, size):
        self.native_book = size


def test_write_empty_array():
    test_string = "somebook"
    writer = MyWriter(test_string, "somesheet", "somename")
    writer.write_array([])
    eq_(test_string, writer._native_book)
