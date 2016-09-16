import datetime

from ._compact import PY2
from ._compact import is_string
from . import constants


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


def from_query_sets(column_names, query_sets,
                    row_renderer=None,
                    skip_row_func=_index_filter, start_row=0, row_limit=-1):
    """
    Convert query sets into an array
    """
    if start_row == 0:
        yield column_names
    for row_index, row in enumerate(query_sets):
        if skip_row_func is not None:
            # + 1 means: column_names were counted in as one row
            row_position = skip_row_func(row_index + 1, start_row, row_limit)
            if row_position == constants.SKIP_DATA:
                continue
            elif row_position == constants.STOP_ITERATION:
                break

        new_array = []
        for column_index, column in enumerate(column_names):
            if '__' in column:
                value = _get_complex_attribute(row, column)
            else:
                value = _get_simple_attribute(row, column)
            new_array.append(value)
        if row_renderer:
            new_array = row_renderer(new_array)
        yield new_array


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


def resolve_missing_readers(extension):
    return resolve_missing_extensions(extension, AVAILABLE_READERS)


def resolve_missing_writers(extension):
    return resolve_missing_extensions(extension, AVAILABLE_WRITERS)


def resolve_missing_extensions(extension, available_list):
    handler = available_list.get(extension)
    message = ""
    if handler:
        if is_string(type(handler)):
            message = constants.MESSAGE_LOADING_FORMATTER % (
                extension, handler)
        else:
            merged = "%s or %s" % (handler[0], handler[1])
            message = constants.MESSAGE_LOADING_FORMATTER % (
                extension, merged)
        raise NotImplementedError(message)
    else:
        raise NotImplementedError()
