import os
from pyexcel_io import CSVZipBook, CSVZipWriter, save_data, OrderedDict, get_io
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


def test_reading_from_memory():
    data = [[1,2,3]]
    io = get_io("csvz")
    zipbook = CSVZipWriter(io)
    sheet = zipbook.create_sheet(None)
    sheet.write_array(data)
    sheet.close()
    zipbook.close()
    zipreader = CSVZipBook(io)
    data = zipreader.sheets()
    assert data['pyexcel_sheet1'] == [['1','2','3']]

        
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
        b = CSVZipBook(self.file, load_sheet_with_name="Sheet 1")
        sheets = b.sheets()
        assert sheets['Sheet 1'] == [
            [u'1.0', u'2.0', u'3.0'],
            [u'4.0', u'5.0', u'6.0'],
            [u'7.0', u'8.0', u'9.0']
        ]
        
    @raises(ValueError)
    def test_read_one_from_many_by_unknown_name(self):
        CSVZipBook(self.file, load_sheet_with_name="Sheet X")

    def test_read_one_from_many_by_index(self):
        b = CSVZipBook(self.file, load_sheet_at_index=0)
        sheets = b.sheets()
        assert sheets['Sheet 1'] == [
            [u'1.0', u'2.0', u'3.0'],
            [u'4.0', u'5.0', u'6.0'],
            [u'7.0', u'8.0', u'9.0']
        ]

    @raises(IndexError)
    def test_read_one_from_many_by_unknown_index(self):
        CSVZipBook(self.file, load_sheet_at_index=999)

    def tearDown(self):
        os.unlink(self.file)

