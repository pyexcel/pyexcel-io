import sys
from pyexcel_io import load_data, StringIO, get_writer, get_io, BytesIO
from nose.tools import raises

PY2 = sys.version_info[0] == 2


@raises(IOError)
def test_wrong_parameter_to_load_data():
    load_data(1)


@raises(IOError)
def test_wrong_parameter_to_get_writer():
    get_writer(1)


@raises(IOError)
def test_wrong_parameter_to_get_writer2():
    get_writer(1, file_type="csv")


@raises(NotImplementedError)
def test_load_ods_data():
    load_data("test.ods")


@raises(NotImplementedError)
def test_load_xls_data_from_memory():
    io = BytesIO()
    load_data(io, file_type="xls")

@raises(IOError)
def test_load_xlsm_data_from_memory():
    if not PY2:
        io = StringIO()
        get_writer(io, file_type="xlsm")
    else:
        raise IOError("pass it")
    
@raises(NotImplementedError)
def test_write_xlsx_data():
    get_writer("test.xlsx")


@raises(IOError)
def test_writer_xlsm_data_from_memory():
    if not PY2:
        io = StringIO()
        get_writer(io, file_type="xlsm")
    else:
        raise IOError("pass it")

@raises(NotImplementedError)
def test_writer_xlsm_data_from_memory2():
    io = BytesIO()
    get_writer(io, file_type="xlsm")


def test_get_io():
    io = get_io("hello")
    assert io == None