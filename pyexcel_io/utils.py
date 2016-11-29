import datetime

from pyexcel_io._compact import PY2
import pyexcel_io.constants as constants


AVAILABLE_READERS = {
    constants.FILE_FORMAT_XLS: 'pyexcel-xls',
    constants.FILE_FORMAT_XLSX: ('pyexcel-xls', 'pyexcel-xlsx'),
    constants.FILE_FORMAT_XLSM: ('pyexcel-xls', 'pyexcel-xlsx'),
    constants.FILE_FORMAT_ODS: ('pyexcel-ods', 'pyexcel-ods3'),
    constants.FILE_FORMAT_CSV: 'pyexcel-io',
    constants.FILE_FORMAT_TSV: 'pyexcel-io',
    constants.FILE_FORMAT_CSVZ: 'pyexcel-io',
    constants.FILE_FORMAT_TSVZ: 'pyexcel-io'
}

AVAILABLE_WRITERS = {
    constants.FILE_FORMAT_XLS: 'pyexcel-xls',
    constants.FILE_FORMAT_XLSX: 'pyexcel-xlsx',
    constants.FILE_FORMAT_XLSM: 'pyexcel-xlsx',
    constants.FILE_FORMAT_ODS: ('pyexcel-ods', 'pyexcel-ods3'),
    constants.FILE_FORMAT_CSV: 'pyexcel-io',
    constants.FILE_FORMAT_TSV: 'pyexcel-io',
    constants.FILE_FORMAT_CSVZ: 'pyexcel-io',
    constants.FILE_FORMAT_TSVZ: 'pyexcel-io'
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
    if PY2:
        return len(filter(lambda element: element != '', array)) == 0
    else:
        return len(list(filter(lambda element: element != '', array))) == 0


def swap_empty_string_for_none(array):
    def swap(x):
        if x == '':
            return None
        else:
            return x
    return [swap(x) for x in array]
