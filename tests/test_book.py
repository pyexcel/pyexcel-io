from pyexcel_io.book import (
    BookReader,
    BookWriter,
    RWInterface,
    _convert_content_to_stream,
)
from pyexcel_io._compact import BytesIO, StringIO

from nose.tools import raises


@raises(NotImplementedError)
def test_rwinterface():
    interface = RWInterface()
    interface.open(1)


@raises(NotImplementedError)
def test_rwinterface_2():
    interface = RWInterface()
    interface.open_stream(1)


@raises(NotImplementedError)
def test_book_reader():
    reader = BookReader()
    reader.read_sheet(1)


@raises(IOError)
def test_book_reader_open_stream():
    reader = BookReader()
    reader.open_stream("a string")


@raises(IOError)
def test_book_writer():
    writer = BookWriter()
    writer.open_stream("a string")


def test_convert_to_bytes_stream():
    file_content = b"test"
    stream = _convert_content_to_stream(file_content, "csv")
    assert isinstance(stream, StringIO)


def test_convert_to_string_stream():
    file_content = "test"
    stream = _convert_content_to_stream(file_content, "csvz")
    assert isinstance(stream, BytesIO)
