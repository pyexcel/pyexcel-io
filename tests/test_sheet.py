from nose.tools import eq_
from pyexcel_io.sheet import SheetWriter, SheetReader
import pyexcel_io.constants as constants


class MyWriter(SheetWriter):
    def set_size(self, size):
        self.native_book = size


class MyReader(SheetReader):
    def number_of_rows(self):
        return len(self._native_sheet)

    def number_of_columns(self):
        return len(self._native_sheet[0])

    def cell_value(self, row, column):
        return self._native_sheet[row][column]


def test_write_empty_array():
    test_string = "somebook"
    writer = MyWriter(test_string, "somesheet", "somename")
    writer.write_array([])
    eq_(test_string, writer._native_book)


def take_second_column(current_index, start, limit=-1):
    decision = constants.SKIP_DATA
    if current_index == 1:
        decision = constants.TAKE_DATA
    elif current_index > 1:
        decision = constants.STOP_ITERATION
    return decision


def test_custom_skip_row_func():
    take_second_row = take_second_column
    array = [[1, 2, 3], [4, 5, 6]]
    reader = MyReader(array, skip_row_func=take_second_row)
    actual = list(reader.to_array())
    expected = [[4, 5, 6]]
    eq_(expected, actual)
    reader.close()


def test_custom_skip_column_func():
    array = [[1, 2, 3], [4, 5, 6]]
    reader = MyReader(array, skip_column_func=take_second_column)
    actual = list(reader.to_array())
    expected = [[2], [5]]
    eq_(expected, actual)
    reader.close()
