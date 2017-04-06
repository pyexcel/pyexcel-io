"""
    pyexcel_io.io
    ~~~~~~~~~~~~~~~~~~~

    The io interface to file extensions

    :copyright: (c) 2014-2017 by Onni Software Ltd.
    :license: New BSD License, see LICENSE for more details
"""
from pyexcel_io._compact import isstream, is_generator, PY2
from pyexcel_io.plugins import iomanager
import pyexcel_io.constants as constants


def get_data(afile, file_type=None, streaming=False, **keywords):
    """Get data from an excel file source

    :param afile: a file name, a file stream or actual content
    :param sheet_name: the name of the sheet to be loaded
    :param sheet_index: the index of the sheet to be loaded
    :param file_type: used only when filename is not a physial file name
    :param streaming: toggles the type of returned data. The values of the
                      returned dictionary remain as generator if it is set
                      to True. Default is False.
    :param library: explicitly name a library for use.
                    e.g. library='pyexcel-ods'
    :param auto_detect_float: defaults to True
    :param auto_detect_int: defaults to True
    :param auto_detect_datetime: defaults to True
    :param ignore_infinity: defaults to True
    :param keywords: any other library specific parameters
    :returns: an ordered dictionary
    """
    if isstream(afile) and file_type is None:
        file_type = constants.FILE_FORMAT_CSV
    if isstream(afile):
        keywords.update(dict(
            file_stream=afile,
            file_type=file_type))
    else:
        if afile is not None and file_type is not None:
            keywords.update(dict(
                file_content=afile,
                file_type=file_type))
        else:
            keywords.update(dict(
                file_name=afile,
                file_type=file_type))
    data = load_data(**keywords)
    if streaming is False:
        for key in data.keys():
            data[key] = list(data[key])
    return data


def save_data(afile, data, file_type=None, **keywords):
    """Save data to an excel file source

    Your data must be a dictionary

    :param filename: actual file name, a file stream or actual content
    :param data: a dictionary but an ordered dictionary is preferred
    :param file_type: used only when filename is not a physial file name
    :param library: explicitly name a library for use.
                    e.g. library='pyexcel-ods'
    :param keywords: any other parameters that python csv module's
                     `fmtparams <https://docs.python.org/release/3.1.5/library/csv.html#dialects-and-formatting-parameters>`_
    """  # noqa
    to_store = data
    if isinstance(data, list) or is_generator(data):
        single_sheet_in_book = True
        to_store = {constants.DEFAULT_SHEET_NAME: data}
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
        file_type = constants.FILE_FORMAT_CSV

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
        keywords.update(dict(
            file_stream=afile,
            file_type=file_type
        ))
    else:
        keywords.update(dict(
            file_name=afile,
            file_type=file_type
        ))
    with get_writer(**keywords) as writer:
        writer.write(data)


def load_data(file_name=None,
              file_content=None,
              file_stream=None,
              file_type=None,
              sheet_name=None,
              sheet_index=None,
              library=None,
              **keywords):
    """Load data from any supported excel formats

    :param filename: actual file name, a file stream or actual content
    :param file_type: used only when filename is not a physial file name
    :param sheet_name: the name of the sheet to be loaded
    :param sheet_index: the index of the sheet to be loaded
    :param keywords: any other parameters
    """
    result = {}
    inputs = [file_name, file_content, file_stream]
    number_of_none_inputs = [x for x in inputs if x is not None]
    if len(number_of_none_inputs) != 1:
        raise IOError(constants.MESSAGE_ERROR_02)
    if file_type is None:
        try:
            file_type = file_name.split(".")[-1]
        except AttributeError:
            raise Exception("file_name should be a string type")
    with iomanager.get_a_plugin('read', file_type, library) as reader:
        if file_name:
            reader.open(file_name, **keywords)
        elif file_content:
            reader.open_content(file_content, **keywords)
        elif file_stream:
            reader.open_stream(file_stream, **keywords)
        if sheet_name:
            result = reader.read_sheet_by_name(sheet_name)
        elif sheet_index is not None:
            result = reader.read_sheet_by_index(sheet_index)
        else:
            result = reader.read_all()
    return result


def get_writer(file_name=None, file_stream=None,
               file_type=None, library=None, **keywords):
    number_of_none_inputs = list(filter(lambda x: x is not None,
                                        [file_name, file_stream]))

    if len(number_of_none_inputs) != 1:
        raise IOError(constants.MESSAGE_ERROR_02)
    file_type_given = True
    if file_type is None and file_name:
        try:
            file_type = file_name.split(".")[-1]
        except AttributeError:
            raise Exception("file_name should be a string type")
        file_type_given = False

    writer = iomanager.get_a_plugin('write', file_type, library)
    if file_name:
        if file_type_given:
            writer.open_content(file_name, **keywords)
        else:
            writer.open(file_name, **keywords)
    elif file_stream:
        writer.open_stream(file_stream, **keywords)
    # else: is resolved by earlier raise statement
    return writer
