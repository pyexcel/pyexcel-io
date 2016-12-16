from nose.tools import raises
from pyexcel_io.book import RWInterface, BookReader, BookWriter


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
