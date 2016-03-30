import os
from pyexcel_io._compact import OrderedDict
from pyexcel_io import save_data
from pyexcel_io.manager import RWManager
from pyexcel_io.csvzipbook import CSVZipBookReader, CSVZipBookWriter
from pyexcel_io.csvzipbook import TSVZipBookReader, TSVZipBookWriter
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
        zipbook = CSVZipBookWriter()
        zipbook.open(self.file)
        zipbook.write({None: data})
        zipbook.close()
        zip = zipfile.ZipFile(self.file, 'r')
        assert zip.namelist() == [file_name]
        content = zip.read(file_name)
        if not PY2:
            content = content.decode('utf-8')
        assert content.replace('\r','').strip('\n') == "1,2,3"
        zip.close()    

    def test_reading(self):
        data = [[1,2,3]]
        zipbook = CSVZipBookWriter()
        zipbook.open(self.file)
        zipbook.write({None: data})
        zipbook.close()
        zipreader = CSVZipBookReader()
        zipreader.open(self.file)
        data = zipreader.read_all()
        assert list(data['pyexcel_sheet1']) == [['1','2','3']]
        zipreader.close()
        
    def tearDown(self):
        os.unlink(self.file)


class TestTSVZ:
    def setUp(self):
        self.file = "tsv.tsvz"

    def test_writing(self):
        data = [[1,2,3]]
        file_name = 'pyexcel_sheet1.tsv'
        zipbook = TSVZipBookWriter()
        zipbook.open(self.file)
        zipbook.write({None: data})
        zipbook.close()
        zip = zipfile.ZipFile(self.file, 'r')
        assert zip.namelist() == [file_name]
        content = zip.read(file_name)
        if not PY2:
            content = content.decode('utf-8')
        assert content.replace('\r','').strip('\n') == "1\t2\t3"
        zip.close()

    def test_reading(self):
        data = [[1,2,3]]
        zipbook = TSVZipBookWriter()
        zipbook.open(self.file)
        zipbook.write({None: data})
        zipbook.close()
        zipreader = TSVZipBookReader()
        zipreader.open(self.file)
        data = zipreader.read_all()
        assert list(data['pyexcel_sheet1']) == [['1','2','3']]
        zipreader.close()

    def tearDown(self):
        os.unlink(self.file)


def test_reading_from_memory():
    data = [[1,2,3]]
    io = RWManager.get_io("csvz")
    zipbook = CSVZipBookWriter()
    zipbook.open_stream(io)
    zipbook.write({None: data})
    zipbook.close()
    zipreader = CSVZipBookReader()
    zipreader.open_stream(io)
    data = zipreader.read_all()
    assert list(data['pyexcel_sheet1']) == [['1','2','3']]

        
class TestMultipleSheet:
    def setUp(self):
        self.content = OrderedDict()
        self.content.update({
            'Sheet 1': 
                [
                    [1.0, 2.0, 3.0], 
                    [4.0, 5.0, 6.0], 
                    [7.0, 8.0, 9.0]
                ]
        })
        self.content.update({
            'Sheet 2': 
                [
                    ['X', 'Y', 'Z'], 
                    [1.0, 2.0, 3.0], 
                    [4.0, 5.0, 6.0]
                ]
        })
        self.content.update({
            'Sheet 3': 
                [
                    ['O', 'P', 'Q'], 
                    [3.0, 2.0, 1.0], 
                    [4.0, 3.0, 2.0]
                ] 
        })
        self.file="mybook.csvz"
        save_data(self.file, self.content)

    def test_read_one_from_many_by_name(self):
        reader = CSVZipBookReader()
        reader.open(self.file)
        sheets = reader.read_sheet_by_name("Sheet 1")
        assert list(sheets['Sheet 1']) == [
            [u'1.0', u'2.0', u'3.0'],
            [u'4.0', u'5.0', u'6.0'],
            [u'7.0', u'8.0', u'9.0']
        ]
        
    @raises(ValueError)
    def test_read_one_from_many_by_unknown_name(self):
        reader = CSVZipBookReader()
        reader.open(self.file)
        reader.read_sheet_by_name("Sheet X")

    def test_read_one_from_many_by_index(self):
        reader = CSVZipBookReader()
        reader.open(self.file)
        sheets = reader.read_sheet_by_index(0)
        assert list(sheets['Sheet 1']) == [
            [u'1.0', u'2.0', u'3.0'],
            [u'4.0', u'5.0', u'6.0'],
            [u'7.0', u'8.0', u'9.0']
        ]

    @raises(IndexError)
    def test_read_one_from_many_by_unknown_index(self):
        reader = CSVZipBookReader()
        reader.open(self.file)
        reader.read_sheet_by_index(9999)


    def tearDown(self):
        os.unlink(self.file)

