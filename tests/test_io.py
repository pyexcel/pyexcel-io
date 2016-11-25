import os
import sys
from unittest import TestCase
from pyexcel_io.deprecated import load_data, get_writer
import pyexcel_io.manager as manager
from pyexcel_io._compact import StringIO, BytesIO, is_string
from pyexcel_io._compact import OrderedDict
from pyexcel_io import save_data, get_data
from pyexcel_io.io import load_data_new, get_writer_new
from nose.tools import raises, eq_
from zipfile import BadZipfile


PY2 = sys.version_info[0] == 2


@raises(NotImplementedError)
def test_not_implemented_1():
    load_data("something")


@raises(NotImplementedError)
def test_not_implemented_2():
    get_writer("something")


@raises(IOError)
def test_no_valid_parameters():
    load_data_new()


@raises(IOError)
def test_no_valid_parameters_2():
    get_writer_new()


@raises(IOError)
def test_none_type_load_data():
    get_data(None)


@raises(Exception)
def test_wrong_parameter_to_get_data():
    get_data(1)


@raises(Exception)
def test_wrong_parameter_to_get_writer():
    get_writer_new(1)


@raises(NotImplementedError)
def test_wrong_parameter_to_get_writer2():
    get_writer_new(1, file_type="csv")


@raises(IOError)
def test_load_ods_data():
    get_data("test.ods")


@raises(IOError)
def test_load_ods_data_from_memory():
    io = BytesIO()
    get_data(io, file_type="ods")


@raises(IOError)
def test_load_unknown_data():
    get_data("test.unknown")


@raises(IOError)
def test_load_unknown_data_from_memory():
    io = BytesIO()
    get_data(io, file_type="unknown")


@raises(BadZipfile)
def test_load_csvz_data_from_memory():
    if not PY2:
        io = StringIO()
        get_data(io, file_type="csvz")
    else:
        raise BadZipfile("pass it")


@raises(IOError)
def test_write_xlsx_data():
    get_data("test.xlsx")


@raises(IOError)
def test_write_unknown_data():
    get_data("test.unknown")


@raises(NotImplementedError)
def test_writer_csvz_data_from_memory():
    if not PY2:
        io = StringIO()
        writer = get_writer_new(io, file_type="csvz")
        writer.write({'adb': [[2, 3]]})
    else:
        raise NotImplementedError("pass it")


@raises(IOError)
def test_writer_xlsm_data_from_memory2():
    io = BytesIO()
    get_writer_new(io, file_type="xlsms")


@raises(IOError)
def test_writer_unknown_data_from_memory2():
    io = BytesIO()
    # mock it
    manager.register_file_type_as_binary_stream('unknown1')
    get_writer_new(io, file_type="unknown1")


def test_get_io():
    io = manager.get_io("hello")
    assert io is None


def test_default_csv_format():
    data = [['1', '2', '3']]
    io = manager.get_io("csv")
    # test default format for saving is 'csv'
    save_data(io, data)
    io.seek(0)
    # test default format for reading is 'csv'
    result = get_data(io)
    assert result['csv'] == [[1, 2, 3]]


def test_file_handle_as_input():
    test_file = "file_handle.csv"
    with open(test_file, 'w') as f:
        f.write("1,2,3")

    with open(test_file, 'r') as f:
        data = get_data(f, 'csv')
        eq_(data['csv'], [[1, 2, 3]])


def test_file_handle_as_output():
    test_file = "file_handle.csv"
    with open(test_file, 'w') as f:
        save_data(f, [[1, 2, 3]], 'csv', lineterminator='\n')

    with open(test_file, 'r') as f:
        content = f.read()
        eq_(content, '1,2,3\n')


def test_binary_file_content():
    data = [['1', '2', '3']]
    io = manager.get_io("csvz")
    save_data(io, data, 'csvz')
    result = get_data(io.getvalue(), 'csvz')
    assert result['pyexcel_sheet1'] == [[1, 2, 3]]


def test_text_file_content():
    data = [['1', '2', '3']]
    io = manager.get_io("csv")
    save_data(io, data, 'csv')
    result = get_data(io.getvalue(), 'csv')
    assert result['csv'] == [[1, 2, 3]]


def test_library_parameter():
    data = [['1', '2', '3']]
    io = manager.get_io("csv")
    save_data(io, data, 'csv', library="built-in")
    result = get_data(io.getvalue(), 'csv', library="built-in")
    assert result['csv'] == [[1, 2, 3]]


def test_conversion_from_bytes_to_text():
    test_file = "conversion.csv"
    data = [['1', '2', '3']]
    save_data(test_file, data)
    with open(test_file, "rb") as f:
        content = f.read()
        result = get_data(content, 'csv')
        assert result['csv'] == [[1, 2, 3]]
    os.unlink(test_file)


def test_is_string():
    if PY2:
        assert is_string(type(u'a')) is True
    else:
        assert is_string(type('a')) is True


@raises(TypeError)
def test_generator_is_obtained():
    data = get_data(os.path.join("tests", "fixtures", "test.csv"),
                    streaming=True)
    len(data['test.csv'])


def test_generator_can_be_written():
    test_filename = "generator.csv"
    test_fixture = os.path.join("tests", "fixtures", "test.csv")
    data = get_data(test_fixture, streaming=True)
    save_data(test_filename, data)
    assert os.path.exists(test_filename)
    data2 = get_data(test_filename)
    expected = get_data(test_fixture)
    assert data2[test_filename] == expected['test.csv']
    os.unlink(test_filename)


class TestReadMultipleSheets(TestCase):
    file_type = "csv"
    delimiter = ','

    def setUp(self):
        self.test_file_formatter = "csv_multiple__%s__%s." + self.file_type
        self.merged_book_file = "csv_multiple." + self.file_type
        self.data = [
            ["1", "2", "3"],
            ["4", "5", "6"],
            ["7", "8", "9"]
        ]
        self.expected_data = [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9]
        ]
        self.sheets = OrderedDict()
        self.sheets.update({"sheet1": self.data})
        self.sheets.update({"sheet2": self.data})
        self.sheets.update({"sheet3": self.data})
        self.expected_sheets = OrderedDict()
        self.expected_sheets.update({"sheet1": self.expected_data})
        self.expected_sheets.update({"sheet2": self.expected_data})
        self.expected_sheets.update({"sheet3": self.expected_data})
        index = 0
        for key, value in self.sheets.items():
            file_name = self.test_file_formatter % (key, index)
            with open(file_name, 'w') as f:
                for row in value:
                    f.write(self.delimiter.join(row) + "\n")
            index = index + 1

    def test_sheet_name(self):
        sheets = get_data(self.merged_book_file, sheet_name="sheet1")
        self.assertEqual(sheets['sheet1'], self.expected_sheets['sheet1'])

    def test_sheet_index(self):
        sheets = get_data(self.merged_book_file, sheet_index=1)
        self.assertEqual(sheets['sheet2'], self.expected_sheets['sheet2'])

    def tearDown(self):
        index = 0
        for key, value in self.sheets.items():
            file_name = self.test_file_formatter % (key, index)
            os.unlink(file_name)
            index = index + 1
