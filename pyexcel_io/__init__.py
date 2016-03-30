"""
    pyexcel_io
    ~~~~~~~~~~~~~~~~~~~

    Uniform interface for reading/writing different excel file formats

    :copyright: (c) 2014-2016 by Onni Software Ltd.
    :license: New BSD License, see LICENSE for more details
"""
import pyexcel_io.fileformat.csv
import pyexcel_io.fileformat.tsv
import pyexcel_io.fileformat.csvz
import pyexcel_io.fileformat.tsvz
import pyexcel_io.database.sql
import pyexcel_io.database.django
from .manager import RWManager
from .io import load_data_new, get_writer_new

from ._compact import isstream, is_generator, PY2
from .constants import (
    FILE_FORMAT_CSV,
    DEFAULT_SHEET_NAME
)


def get_data(afile, file_type=None, streaming=False, **keywords):
    """Get data from an excel file source

    :param filename: actual file name, a file stream or actual content
    :param sheet_name: the name of the sheet to be loaded
    :param sheet_index: the index of the sheet to be loaded
    :param file_type: used only when filename is not a physial file name
    :param keywords: any other parameters
    :returns: an array if it is a single sheet, an ordered dictionary otherwise
    """
    if isstream(afile) and file_type is None:
        file_type = FILE_FORMAT_CSV
    if isstream(afile):
        data = load_data_new(file_stream=afile, file_type=file_type, **keywords)
    else:
        if afile is not None and file_type is not None:
            data = load_data_new(file_content=afile, file_type=file_type, **keywords)
        else:
            data = load_data_new(file_name=afile, file_type=file_type, **keywords)
    if streaming is False:
        for key in data.keys():
            data[key] = list(data[key])
    return data


def save_data(afile, data, file_type=None, **keywords):
    """Save data to an excel file source

    Your data can be an array or an ordered dictionary

    :param filename: actual file name, a file stream or actual content
    :param data: the data to be saved
    :param file_type: used only when filename is not a physial file name
    :param keywords: any other parameters that python csv module's
                     `fmtparams <https://docs.python.org/release/3.1.5/
                      library/csv.html#dialects-and-formatting-parameters>`_
    """
    to_store = data
    if isinstance(data, list) or is_generator(data):
        single_sheet_in_book = True
        to_store = {DEFAULT_SHEET_NAME: data}
    else:
        if PY2:
            keys = data.keys()
        else:
            keys = list(data.keys())
        if len(keys) == 1:
            single_sheet_in_book = True
        else:
            single_sheet_in_book = False

    if isstream(afile) and file_type is None:
        file_type = FILE_FORMAT_CSV

    store_data(afile, to_store,
               file_type=file_type,
               single_sheet_in_book=single_sheet_in_book,
               **keywords)

def store_data(afile, data, file_type=None, **keywords):
    """Non public function to store data to afile

    :param filename: actual file name, a file stream or actual content
    :param data: the data to be written
    :param file_type: used only when filename is not a physial file name
    :param keywords: any other parameters
    """
    if isstream(afile):
        writer = get_writer_new(
            file_stream=afile,
            file_type=file_type,
            **keywords)
    else:
        writer = get_writer_new(
            file_name=afile,
            file_type=file_type,
            **keywords)
    writer.write(data)
    writer.close()


try:
    import pyexcel_xls
    pyexcel_xls.extend_pyexcel(RWManager)
except Exception as e:
    print(e)
    pass


try:
    import pyexcel_xlsx
    pyexcel_xlsx.extend_pyexcel(RWManager)
except:
    pass


try:
    import pyexcel_ods3
    pyexcel_ods3.extend_pyexcel(RWManager)
except:
    pass

