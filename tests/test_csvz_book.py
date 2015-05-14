import os
from pyexcel_io import CSVZipBook, CSVZipWriter
from nose.tools import raises
import zipfile

class TestCVSZReading:
    def setUp(self):
        self.file = "csvz.csvz"

    def test_writing(self):
        data = [[1,2,3]]
        zipbook = CSVZipWriter(self.file)
        sheet = zipbook.create_sheet(None)
        sheet.write_array(data)
        sheet.close()
        zipbook.close()
        zip = zipfile.ZipFile(self.file, 'r')
        assert zip.namelist() == ['pyexcel_sheet.csv']
