"""
    pyexcel_io.utils
    ~~~~~~~~~~~~~~~~~~~

    utility functions

    :copyright: (c) 2014-2017 by Onni Software Ltd.
    :license: New BSD License, see LICENSE for more details
"""
import datetime

import pyexcel_io.constants as constants


XLS_PLUGIN = 'pyexcel-xls'
XLSX_PLUGIN = 'pyexcel-xlsx'
ODS_PLUGIN = 'pyexcel-ods'
ODS3_PLUGIN = 'pyexcel-ods3'
XLSXW_PLUGIN = 'pyexcel-xlsxw'
IO_ITSELF = 'pyexcel-io'


AVAILABLE_READERS = {
    constants.FILE_FORMAT_XLS: [XLS_PLUGIN],
    constants.FILE_FORMAT_XLSX: [XLS_PLUGIN, XLSX_PLUGIN],
    constants.FILE_FORMAT_XLSM: [XLS_PLUGIN, XLSX_PLUGIN],
    constants.FILE_FORMAT_ODS: [ODS_PLUGIN, ODS3_PLUGIN],
    constants.FILE_FORMAT_CSV: [IO_ITSELF],
    constants.FILE_FORMAT_TSV: [IO_ITSELF],
    constants.FILE_FORMAT_CSVZ: [IO_ITSELF],
    constants.FILE_FORMAT_TSVZ: [IO_ITSELF]
}

AVAILABLE_WRITERS = {
    constants.FILE_FORMAT_XLS: [XLS_PLUGIN],
    constants.FILE_FORMAT_XLSX: [XLSX_PLUGIN, XLSXW_PLUGIN],
    constants.FILE_FORMAT_XLSM: [XLSX_PLUGIN],
    constants.FILE_FORMAT_ODS: [ODS_PLUGIN, ODS3_PLUGIN],
    constants.FILE_FORMAT_CSV: [IO_ITSELF],
    constants.FILE_FORMAT_TSV: [IO_ITSELF],
    constants.FILE_FORMAT_CSVZ: [IO_ITSELF],
    constants.FILE_FORMAT_TSVZ: [IO_ITSELF]
}


def _index_filter(current_index, start, limit=-1):
    out_range = constants.SKIP_DATA
    if current_index >= start:
        out_range = constants.TAKE_DATA
    if limit > 0 and out_range == constants.TAKE_DATA:
        if current_index >= (start + limit):
            out_range = constants.STOP_ITERATION
    return out_range


def _get_complex_attribute(row, attribute):
    attributes = attribute.split('__')
    value = row
    try:
        for attributee in attributes:
            value = _get_simple_attribute(value, attributee)
    except AttributeError:
        value = None
    return value


def _get_simple_attribute(row, attribute):
    value = getattr(row, attribute)
    if isinstance(value, (datetime.date, datetime.time)):
        value = value.isoformat()
    return value


def is_empty_array(array):
    """
    Check if an array is an array of '' or not
    """
    empty_array = [element for element in array if element != '']
    return len(empty_array) == 0


def swap_empty_string_for_none(array):
    """ replace empty string fields with None """
    def swap(value):
        if value == '':
            return None
        else:
            return value
    return [swap(x) for x in array]
