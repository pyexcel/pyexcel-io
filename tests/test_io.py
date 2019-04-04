import os
import sys
import types
from unittest import TestCase
import pyexcel_io.manager as manager
import pyexcel_io.exceptions as exceptions
from pyexcel_io._compact import StringIO, BytesIO, is_string
from pyexcel_io._compact import OrderedDict
from pyexcel_io import save_data, get_data, iget_data
from pyexcel_io.io import load_data, get_writer
from nose.tools import raises, eq_
from zipfile import BadZipfile


PY2 = sys.version_info[0] == 2


def test_force_file_type():
    test_file = "force_file_type.txt"
    data = get_data(
        os.path.join("tests", "fixtures", test_file), force_file_type="csv"
    )
    expected = [[1, 2, 3]]
    eq_(expected, data[test_file])


@raises(IOError)
def test_invalid_file():
    load_data('/something/does/not/exist')


@raises(IOError)
def test_no_valid_parameters():
    load_data()


@raises(IOError)
def test_no_valid_parameters_2():
    get_writer()


@raises(IOError)
def test_none_type_load_data():
    get_data(None)


@raises(Exception)
def test_wrong_parameter_to_get_data():
    get_data(1)


@raises(Exception)
def test_wrong_parameter_to_get_writer():
    get_writer(1)


@raises(Exception)
def test_wrong_parameter_to_get_writer2():
    get_writer(1, file_type="csv")


def test_load_ods_data():
    msg = "Please install one of these plugins for read data in 'ods': "
    msg += "pyexcel-ods,pyexcel-ods3"
    try:
        get_data("test.ods")
    except exceptions.SupportingPluginAvailableButNotInstalled as e:
        eq_(str(e), msg)


def test_load_ods_data_from_memory():
    io = BytesIO()
    msg = "Please install one of these plugins for read data in 'ods': "
    msg += "pyexcel-ods,pyexcel-ods3"
    try:
        get_data(io, file_type="ods")
    except exceptions.SupportingPluginAvailableButNotInstalled as e:
        eq_(str(e), msg)


def test_write_xlsx_data_to_memory():
    data = {"Sheet": [[1]]}
    io = BytesIO()
    msg = "Please install one of these plugins for write data in 'xlsx': "
    msg += "pyexcel-xlsx,pyexcel-xlsxw"
    try:
        save_data(io, data, file_type="xlsx")
    except exceptions.SupportingPluginAvailableButNotInstalled as e:
        eq_(str(e), msg)


@raises(IOError)
def test_load_unknown_data():
    get_data("test.unknown")


@raises(exceptions.NoSupportingPluginFound)
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


@raises(Exception)
def test_writer_csvz_data_from_memory():
    if not PY2:
        io = StringIO()
        writer = get_writer(io, file_type="csvz")
        writer.write({"adb": [[2, 3]]})
    else:
        raise Exception("pass it")


@raises(exceptions.NoSupportingPluginFound)
def test_writer_xlsm_data_from_memory2():
    io = BytesIO()
    get_writer(io, file_type="xlsms")


@raises(exceptions.NoSupportingPluginFound)
def test_writer_unknown_data_from_memory2():
    io = BytesIO()
    # mock it
    manager.register_stream_type("unknown1", "text")
    get_writer(io, file_type="unknown1")


def test_get_io():
    io = manager.get_io("hello")
    assert io is None


def test_get_io_type():
    t = manager.get_io_type("hello")
    assert t is None
    t = manager.get_io_type("csv")
    eq_(t, "string")
    t = manager.get_io_type("xls")
    eq_(t, "bytes")


def test_default_csv_format():
    data = [["1", "2", "3"]]
    io = manager.get_io("csv")
    # test default format for saving is 'csv'
    save_data(io, data)
    io.seek(0)
    # test default format for reading is 'csv'
    result = get_data(io)
    assert result["csv"] == [[1, 2, 3]]


def test_case_insentivity():
    data = [["1", "2", "3"]]
    io = manager.get_io("CSV")
    # test default format for saving is 'csv'
    save_data(io, data)
    io.seek(0)
    # test default format for reading is 'csv'
    result = get_data(io)
    assert result["csv"] == [[1, 2, 3]]


def test_file_handle_as_input():
    test_file = "file_handle.csv"
    with open(test_file, "w") as f:
        f.write("1,2,3")

    with open(test_file, "r") as f:
        data = get_data(f, "csv")
        eq_(data["csv"], [[1, 2, 3]])


def test_file_type_case_insensitivity():
    test_file = "file_handle.CSv"
    with open(test_file, "w") as f:
        f.write("1,2,3")

    with open(test_file, "r") as f:
        data = get_data(f, "csv")
        eq_(data["csv"], [[1, 2, 3]])


def test_file_handle_as_output():
    test_file = "file_handle.csv"
    with open(test_file, "w") as f:
        save_data(f, [[1, 2, 3]], "csv", lineterminator="\n")

    with open(test_file, "r") as f:
        content = f.read()
        eq_(content, "1,2,3\n")


def test_binary_file_content():
    data = [["1", "2", "3"]]
    io = manager.get_io("csvz")
    save_data(io, data, "csvz")
    result = get_data(io.getvalue(), "csvz")
    eq_(result["pyexcel_sheet1"], [[1, 2, 3]])


def test_text_file_content():
    data = [["1", "2", "3"]]
    io = manager.get_io("csv")
    save_data(io, data, "csv")
    result = get_data(io.getvalue(), "csv")
    eq_(result["csv"], [[1, 2, 3]])


def test_library_parameter():
    data = [["1", "2", "3"]]
    io = manager.get_io("csv")
    save_data(io, data, "csv", library="pyexcel-io")
    result = get_data(io.getvalue(), "csv", library="pyexcel-io")
    eq_(result["csv"], [[1, 2, 3]])


@raises(Exception)
def test_library_parameter_error_situation():
    data = [["1", "2", "3"]]
    io = manager.get_io("csv")
    save_data(io, data, "csv", library="doesnot-exist")


def test_conversion_from_bytes_to_text():
    test_file = "conversion.csv"
    data = [["1", "2", "3"]]
    save_data(test_file, data)
    with open(test_file, "rb") as f:
        content = f.read()
        result = get_data(content, "csv")
        assert result["csv"] == [[1, 2, 3]]
    os.unlink(test_file)


def test_is_string():
    if PY2:
        assert is_string(type(u"a")) is True
    else:
        assert is_string(type("a")) is True


def test_generator_is_obtained():
    data, reader = iget_data(os.path.join("tests", "fixtures", "test.csv"))
    assert isinstance(data["test.csv"], types.GeneratorType)
    reader.close()


def test_generator_can_be_written():
    test_filename = "generator.csv"
    test_fixture = os.path.join("tests", "fixtures", "test.csv")
    data = get_data(test_fixture, streaming=True)
    save_data(test_filename, data)
    assert os.path.exists(test_filename)
    data2 = get_data(test_filename)
    expected = get_data(test_fixture)
    assert data2[test_filename] == expected["test.csv"]
    os.unlink(test_filename)


class TestReadMultipleSheets(TestCase):
    file_type = "csv"
    delimiter = ","

    def setUp(self):
        self.test_file_formatter = "csv_multiple__%s__%s." + self.file_type
        self.merged_book_file = "csv_multiple." + self.file_type
        self.data = [["1", "2", "3"], ["4", "5", "6"], ["7", "8", "9"]]
        self.expected_data = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
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
            with open(file_name, "w") as f:
                for row in value:
                    f.write(self.delimiter.join(row) + "\n")
            index = index + 1

    def test_sheet_name(self):
        sheets = get_data(self.merged_book_file, sheet_name="sheet1")
        eq_(sheets["sheet1"], self.expected_sheets["sheet1"])

    def test_sheet_index(self):
        sheets = get_data(self.merged_book_file, sheet_index=1)
        eq_(sheets["sheet2"], self.expected_sheets["sheet2"])

    def test_read_many(self):
        sheets = get_data(self.merged_book_file, sheets=["sheet1", 2])
        eq_(sheets["sheet1"], self.expected_sheets["sheet1"])
        eq_(sheets["sheet3"], self.expected_sheets["sheet3"])
        assert "sheet2" not in sheets

    def tearDown(self):
        index = 0
        for key, value in self.sheets.items():
            file_name = self.test_file_formatter % (key, index)
            os.unlink(file_name)
            index = index + 1
