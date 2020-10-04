from pyexcel_io.plugin_api import ISheet, IReader, IWriter, ISheetWriter

from nose.tools import raises


class TestISheet:
    def setUp(self):
        self.isheet = ISheet()

    @raises(NotImplementedError)
    def test_row_iterator(self):
        self.isheet.row_iterator()

    @raises(NotImplementedError)
    def test_column_iterator(self):
        self.isheet.column_iterator(1)


class TestISheetWriter:
    def setUp(self):
        self.isheet_writer = ISheetWriter()

    @raises(NotImplementedError)
    def test_write_row(self):
        self.isheet_writer.write_row([1, 2])


class TestIReader:
    def setUp(self):
        self.ireader = IReader()

    @raises(NotImplementedError)
    def test_read_sheet(self):
        self.ireader.read_sheet(1)


class TestIWriter:
    def setUp(self):
        self.iwriter = IWriter()

    @raises(NotImplementedError)
    def test_create_sheet(self):
        self.iwriter.create_sheet("a name")


@raises(Exception)
def test_empty_writer():
    class TestWriter(IWriter):
        def create_sheet(self, sheet_name):
            return None

    test_writer = TestWriter()
    test_writer.write({"sheet 1": [[1, 2]]})
