import datetime

from ._compact import PY2
from ._compact import is_string
from .constants import (
    FILE_FORMAT_ODS,
    FILE_FORMAT_XLS,
    FILE_FORMAT_XLSX,
    FILE_FORMAT_XLSM,
    MESSAGE_LOADING_FORMATTER
)


AVAILABLE_READERS = {
    FILE_FORMAT_XLS: 'pyexcel-xls',
    FILE_FORMAT_XLSX: ('pyexcel-xls', 'pyexcel-xlsx'),
    FILE_FORMAT_XLSM: ('pyexcel-xls', 'pyexcel-xlsx'),
    FILE_FORMAT_ODS: ('pyexcel-ods', 'pyexcel-ods3')
}

AVAILABLE_WRITERS = {
    FILE_FORMAT_XLS: 'pyexcel-xls',
    FILE_FORMAT_XLSX: 'pyexcel-xlsx',
    FILE_FORMAT_XLSM: 'pyexcel-xlsx',
    FILE_FORMAT_ODS: ('pyexcel-ods', 'pyexcel-ods3')
}



def from_query_sets(column_names, query_sets):
    """
    Convert query sets into an array
    """
    yield column_names
    for row in query_sets:
        new_array = []
        for column in column_names:
            value = getattr(row, column)
            if isinstance(value, (datetime.date, datetime.time)):
                value = value.isoformat()
            new_array.append(value)
        yield new_array


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


def resolve_missing_readers(extension):
    return resolve_missing_extensions(extension, AVAILABLE_READERS)


def resolve_missing_writers(extension):
    return resolve_missing_extensions(extension, AVAILABLE_WRITERS)


def resolve_missing_extensions(extension, available_list):
    handler = available_list.get(extension)
    message = ""
    if handler:
        if is_string(type(handler)):
            message = MESSAGE_LOADING_FORMATTER % (extension, handler)
        else:
            merged = "%s or %s" % (handler[0], handler[1])
            message = MESSAGE_LOADING_FORMATTER % (extension, merged)
        raise NotImplementedError(message)
    else:
        raise NotImplementedError()


