import os
from pyexcel_io import CSVZipBook, CSVZipWriter
import zipfile

class TestCSVZ:
    def setUp(self):
        self.file = "csvz.csvz"

    def test_writing(self):
        data = [[1,2,3]]
        file_name = 'pyexcel_sheet1.csv'
        zipbook = CSVZipWriter(self.file)
        sheet = zipbook.create_sheet(None)
        sheet.write_array(data)
        sheet.close()
        zipbook.close()
        zip = zipfile.ZipFile(self.file, 'r')
        assert zip.namelist() == [file_name]
        content = zip.read(file_name)
        assert content.replace('\r','').strip('\n') == "1,2,3"

    def test_reading(self):
        data = [[1,2,3]]
        zipbook = CSVZipWriter(self.file)
        sheet = zipbook.create_sheet(None)
        sheet.write_array(data)
        sheet.close()
        zipbook.close()
        zipreader = CSVZipBook(self.file)
        data = zipreader.sheets()
        assert data['pyexcel_sheet1'] == [['1','2','3']]

    def tearDown(self):
        os.unlink(self.file)
