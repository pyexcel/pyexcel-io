from nose.tools import eq_, raises
from pyexcel_io.service import date_value, time_value


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
    result = time_value('PT1111')
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
    result = time_value('PT1111')
    eq_(result, None)
