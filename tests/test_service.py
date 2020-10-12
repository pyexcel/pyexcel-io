from datetime import time, datetime, timedelta

from pyexcel_io.service import (
    date_value,
    time_value,
    float_value,
    boolean_value,
    ods_bool_value,
    ods_date_value,
    ods_time_value,
    ods_float_value,
    throw_exception,
    detect_int_value,
    detect_float_value,
    ods_timedelta_value,
)
from pyexcel_io.exceptions import IntegerAccuracyLossError

from nose.tools import eq_, raises


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


@raises(IntegerAccuracyLossError)
def test_big_int_value():
    ods_float_value(1000000000000000)


@raises(IntegerAccuracyLossError)
def test_throw_exception():
    throw_exception(1000000000000000)


def test_boolean_value():
    fixture = ["true", "false", 1]
    expected = [True, False, 1]

    actual = [boolean_value(element) for element in fixture]
    eq_(actual, expected)


def test_time_delta_presentation():
    a = datetime(2020, 12, 12, 12, 12, 12)
    b = datetime(2020, 11, 12, 12, 12, 11)
    delta = a - b

    value = ods_timedelta_value(delta)
    eq_(value, "PT720H00M01S")


def test_ods_bool_to_string():
    fixture = [True, False]
    expected = ["true", "false"]

    actual = [ods_bool_value(element) for element in fixture]
    eq_(actual, expected)


def test_ods_time_value():
    test = datetime(2020, 10, 6, 11, 11, 11)
    actual = ods_time_value(test)
    eq_(actual, "PT11H11M11S")


def test_ods_date_value():
    test = datetime(2020, 10, 6, 11, 11, 11)
    actual = ods_date_value(test)
    eq_(actual, "2020-10-06")


def test_time_value_returns_time_delta():
    test_time_value = "PT720H00M01S"
    delta = time_value(test_time_value)
    eq_(delta, timedelta(days=30, seconds=1))


def test_time_value():
    test_time_value = "PT23H00M01S"
    delta = time_value(test_time_value)
    eq_(delta, time(23, 0, 1))


def test_float_value():
    a = float_value("1.2")
    eq_(a, 1.2)
