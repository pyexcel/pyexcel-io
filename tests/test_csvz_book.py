import os
from pyexcel_io import save_data, OrderedDict, get_io
from pyexcel_io.csvzipbook import CSVZipWriter
import zipfile
from nose.tools import raises
import sys
PY2 = sys.version_info[0] == 2


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
        if not PY2:
            content = content.decode('utf-8')
        assert content.replace('\r','').strip('\n') == "1,2,3"
        zip.close()    

    def tearDown(self):
        os.unlink(self.file)

class TestTSVZ:
    def setUp(self):
        self.file = "tsv.tsvz"

    def test_writing(self):
        data = [[1,2,3]]
        file_name = 'pyexcel_sheet1.tsv'
        zipbook = CSVZipWriter(self.file, dialect="excel-tab")
        sheet = zipbook.create_sheet(None)
        sheet.write_array(data)
        sheet.close()
        zipbook.close()
        self.zip = zipfile.ZipFile(self.file, 'r')
        assert self.zip.namelist() == [file_name]
        content = self.zip.read(file_name)
        if not PY2:
            content = content.decode('utf-8')
        assert content.replace('\r','').strip('\n') == "1\t2\t3"

    def tearDown(self):
        self.zip.close()    
        os.unlink(self.file)

