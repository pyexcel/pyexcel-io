import os

from pyexcel_io import get_data, save_data
from pyexcel_io.utils import _index_filter
from nose.tools import eq_
import pyexcel_io.constants as constants


def test_index_filter():
    current_index, start, limit, expected = (0, 1, -1, constants.SKIP_DATA)
    eq_(_index_filter(current_index, start, limit), expected)
    current_index, start, limit, expected = (2, 1, -1, constants.TAKE_DATA)
    eq_(_index_filter(current_index, start, limit), expected)
    current_index, start, limit, expected = (2, 1, 10, constants.TAKE_DATA)
    eq_(_index_filter(current_index, start, limit), expected)
    current_index, start, limit, expected = (
        100,
        1,
        10,
        constants.STOP_ITERATION,
    )
    eq_(_index_filter(current_index, start, limit), expected)


class TestFilter:
    def setUp(self):
        self.test_file = "test_filter.csv"
        sample = [
            [1, 21, 31],
            [2, 22, 32],
            [3, 23, 33],
            [4, 24, 34],
            [5, 25, 35],
            [6, 26, 36],
        ]
        save_data(self.test_file, sample)

    def test_filter_row(self):
        filtered_data = get_data(self.test_file, start_row=3)
        expected = [[4, 24, 34], [5, 25, 35], [6, 26, 36]]
        eq_(filtered_data[self.test_file], expected)

    def test_filter_row_2(self):
        filtered_data = get_data(self.test_file, start_row=3, row_limit=1)
        expected = [[4, 24, 34]]
        eq_(filtered_data[self.test_file], expected)

    def test_filter_column(self):
        filtered_data = get_data(self.test_file, start_column=1)
        expected = [[21, 31], [22, 32], [23, 33], [24, 34], [25, 35], [26, 36]]
        eq_(filtered_data[self.test_file], expected)

    def test_filter_column_2(self):
        filtered_data = get_data(
            self.test_file, start_column=1, column_limit=1
        )
        expected = [[21], [22], [23], [24], [25], [26]]
        eq_(filtered_data[self.test_file], expected)

    def test_filter_both_ways(self):
        filtered_data = get_data(self.test_file, start_column=1, start_row=3)
        expected = [[24, 34], [25, 35], [26, 36]]
        eq_(filtered_data[self.test_file], expected)

    def test_filter_both_ways_2(self):
        filtered_data = get_data(
            self.test_file,
            start_column=1,
            column_limit=1,
            start_row=3,
            row_limit=1,
        )
        expected = [[24]]
        eq_(filtered_data[self.test_file], expected)

    def tearDown(self):
        os.unlink(self.test_file)
