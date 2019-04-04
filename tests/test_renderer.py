import os

from pyexcel_io import get_data, save_data

from nose.tools import eq_


class TestRenderer:
    def setUp(self):
        self.test_file = "test_filter.csv"
        sample = [[1, 21, 31], [2, 22, 32]]
        save_data(self.test_file, sample)

    def test_filter_row(self):
        def custom_row_renderer(row):
            return [str(element) for element in row]

        custom_data = get_data(
            self.test_file, row_renderer=custom_row_renderer
        )
        expected = [["1", "21", "31"], ["2", "22", "32"]]
        eq_(custom_data[self.test_file], expected)

    def tearDown(self):
        os.unlink(self.test_file)
