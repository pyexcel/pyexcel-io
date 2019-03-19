from nose.tools import eq_, raises
from pyexcel_io.service import date_value, time_value
from pyexcel_io.service import detect_int_value
from pyexcel_io.service import detect_float_value
from pyexcel_io.service import ODS_WRITE_FORMAT_COVERSION
from pyexcel_io.service import ods_float_value
from pyexcel_io.service import throw_exception
from pyexcel_io._compact import PY2
from pyexcel_io.exceptions import IntegerAccuracyLossError
from nose import SkipTest


def test_date_util_parse():
    value = "2015-08-17T19:20:00"
    d = date_value(value)
    assert d.strftime("%Y-%m-%dT%H:%M:%S") == "2015-08-17T19:20:00"
    value = "2015-08-17"
    d = date_value(value)
    assert d.strftime("%Y-%m-%d") == "2015-08-17"
    value = "2015-08-17T19:20:59.999999"
    d = date_value(value)
    assert d.strftime("%Y-%m-%dT%H:%M:%S") == "2015-08-17T19:20:59"
    value = "2015-08-17T19:20:59.99999"
    d = date_value(value)
    assert d.strftime("%Y-%m-%dT%H:%M:%S") == "2015-08-17T19:20:59"
    value = "2015-08-17T19:20:59.999999999999999"
    d = date_value(value)
    assert d.strftime("%Y-%m-%dT%H:%M:%S") == "2015-08-17T19:20:59"


def test_issue_8_1():
    # https://github.com/pyexcel/pyexcel-ods3/issues/8
    result = time_value("PT1111")
    eq_(result, None)


@raises(Exception)
def test_invalid_date():
    value = "2015-08-"
    date_value(value)


@raises(Exception)
def test_fake_date_time_10():
    date_value("1234567890")


@raises(Exception)
def test_fake_date_time_19():
    date_value("1234567890123456789")


@raises(Exception)
def test_fake_date_time_20():
    date_value("12345678901234567890")


def test_issue_1_error():
    result = time_value("PT1111")
    eq_(result, None)


def test_detect_int_value():
    result = detect_int_value("123")
    eq_(result, 123)


def test_detect_float_value():
    result = detect_float_value("123.1")
    eq_(result, 123.1)


def test_suppression_of_pep_0515_int():
    result = detect_int_value("123_123")
    eq_(result, None)


def test_suppression_of_pep_0515_float():
    result = detect_float_value("123_123.")
    eq_(result, None)
    result = detect_float_value("123_123.1")
    eq_(result, None)


def test_detect_float_value_on_nan():
    result = detect_float_value("NaN", ignore_nan_text=True)
    eq_(result, None)


def test_detect_float_value_on_custom_nan_text():
    result = detect_float_value("NaN", default_float_nan="nan")
    eq_(result, None)


def test_detect_float_value_on_custom_nan_text2():
    result = detect_float_value("nan", default_float_nan="nan")
    eq_(str(result), "nan")


def test_ods_write_format_conversion():
    if PY2:
        expected = ODS_WRITE_FORMAT_COVERSION[long]  # noqa: F821
        eq_('long', expected)
    else:
        raise SkipTest()


@raises(IntegerAccuracyLossError)
def test_big_int_value():
    ods_float_value(1000000000000000)


def test_max_value_on_python_2():
    if PY2:
        ods_float_value(long(999999999999999))
    else:
        raise SkipTest("No long in python 3")


@raises(IntegerAccuracyLossError)
def test_really_long_value_on_python2():
    if PY2:
        ods_float_value(long(999999999999999+1))
    else:
        raise SkipTest("No long in python 3")


@raises(IntegerAccuracyLossError)
def test_throw_exception():
    throw_exception(1000000000000000)
