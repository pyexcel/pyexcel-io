"""
    pyexcel_io
    ~~~~~~~~~~~~~~~~~~~

    Uniform interface for reading/writing different excel file formats

    :copyright: (c) 2014-2016 by Onni Software Ltd.
    :license: New BSD License, see LICENSE for more details
"""
from functools import partial
from .base import(
    NamedContent,
    SheetReaderBase,
    SheetReader,
    BookReaderBase,
    BookReader,
    SheetWriterBase,
    SheetWriter,
    BookWriter,
    from_query_sets
)
from .csvbook import CSVBook, CSVWriter
from .csvzipbook import CSVZipWriter, CSVZipBook
from .sqlbook import SQLBookReader, SQLBookWriter, PyexcelSQLSkipRowException
from .djangobook import DjangoBookReader, DjangoBookWriter
from ._compact import (
    is_string, BytesIO, StringIO,
    isstream, OrderedDict, PY2,
    is_generator)
from .constants import (
    MESSAGE_LOADING_FORMATTER,
    MESSAGE_ERROR_02,
    MESSAGE_ERROR_03,
    MESSAGE_WRONG_IO_INSTANCE,
    MESSAGE_CANNOT_WRITE_STREAM_FORMATTER,
    MESSAGE_CANNOT_READ_STREAM_FORMATTER,
    MESSAGE_CANNOT_WRITE_FILE_TYPE_FORMATTER,
    MESSAGE_CANNOT_READ_FILE_TYPE_FORMATTER,
    FILE_FORMAT_CSV,
    FILE_FORMAT_TSV,
    FILE_FORMAT_CSVZ,
    FILE_FORMAT_TSVZ,
    FILE_FORMAT_ODS,
    FILE_FORMAT_XLS,
    FILE_FORMAT_XLSX,
    FILE_FORMAT_XLSM,
    DB_SQL,
    DB_DJANGO,
    DEFAULT_SHEET_NAME
)
from .book import (
    ReaderFactory,
    resolve_missing_extensions,
    validate_io,
    get_io,
    BINARY_STREAM_TYPES
)

# A list of registered writers
WRITERS = {
    FILE_FORMAT_CSV: CSVWriter,
    FILE_FORMAT_TSV: partial(CSVWriter, dialect="excel-tab"),
    FILE_FORMAT_CSVZ: CSVZipWriter,
    FILE_FORMAT_TSVZ: partial(CSVZipWriter, dialect="excel-tab"),
    DB_SQL: SQLBookWriter,
    DB_DJANGO: DjangoBookWriter
}

AVAILABLE_WRITERS = {
    FILE_FORMAT_XLS: 'pyexcel-xls',
    FILE_FORMAT_XLSX: 'pyexcel-xlsx',
    FILE_FORMAT_XLSM: 'pyexcel-xlsx',
    FILE_FORMAT_ODS: ('pyexcel-ods', 'pyexcel-ods3')
}

def load_data(filename,
              file_type=None,
              sheet_name=None,
              sheet_index=None,
              **keywords):
    file_name=None
    file_stream=None
    file_content=None
    extension=None
    from_memory=False
    if filename is None:
        raise IOError(MESSAGE_ERROR_02)
    elif not is_string(type(filename)) and not isstream(filename):
        raise IOError(MESSAGE_ERROR_02)
    if file_type is not None:
        from_memory = True
        extension = file_type
    else:
        extension = filename.split(".")[-1]
    if from_memory:
        if isstream(filename):
            file_stream = filename
        else:
            file_content = filename
    else:
        file_name = filename
    try:
        return load_data_new(
            file_name=file_name,
            file_content=file_content,
            file_stream=file_stream,
            file_type=extension,
            sheet_name=sheet_name,
            sheet_index=sheet_index,
            **keywords
        )
    except NotImplementedError:
        if from_memory:
            raise NotImplementedError(
                MESSAGE_CANNOT_READ_STREAM_FORMATTER % extension)
        else:
            raise NotImplementedError(
                MESSAGE_CANNOT_READ_FILE_TYPE_FORMATTER % (extension,
                                                           filename))        

def load_data_new(file_name=None,
                  file_content=None,
                  file_stream=None,
                  file_type=None,
                  sheet_name=None,
                  sheet_index=None,
                  **keywords):
    """Load data from any supported excel formats

    :param filename: actual file name, a file stream or actual content
    :param file_type: used only when filename is not a physial file name
    :param sheet_name: the name of the sheet to be loaded
    :param sheet_index: the index of the sheet to be loaded
    :param keywords: any other parameters
    """
    result = {}
    number_of_none_inputs = list(filter(lambda x: x is not None,
                                        [file_name, file_content, file_stream]))
    if len(number_of_none_inputs) != 1:
        raise IOError(MESSAGE_ERROR_02)
    if file_type is None:
        file_type = file_name.split(".")[-1]
    reader = ReaderFactory.create_reader(file_type)
    if file_name:
        reader.open(file_name, **keywords)
    elif file_content:
        reader.open_content(file_content, **keywords)
    elif file_stream:
        reader.open_stream(file_stream, **keywords)
    if sheet_name:
        result = reader.read_sheet_by_name(sheet_name)
    elif sheet_index:
        result = reader.read_sheet_by_index(sheet_index)
    else:
        result = reader.read_all()
    return result


def get_writer(filename, file_type=None, **keywords):
    """Create a writer from any supported excel formats

    :param filename: actual file name or a file stream
    :param file_type: used only when filename is not a physial file name
    :param keywords: any other parameters
    """
    extension = None
    writer = None
    to_memory = False
    if filename is None:
        raise IOError(MESSAGE_ERROR_02)
    if filename in WRITERS:
        writer_class = WRITERS[filename]
        writer = writer_class(filename, **keywords)
        writer.set_type(filename)
    else:
        if file_type is not None:
            if isstream(filename):
                extension = file_type
                to_memory = True
                if not validate_io(file_type, filename):
                    raise IOError(MESSAGE_WRONG_IO_INSTANCE)
            else:
                raise IOError(MESSAGE_ERROR_03)
        elif is_string(type(filename)):
            extension = filename.split(".")[-1]
        else:
            raise IOError(MESSAGE_ERROR_03)
        if extension in WRITERS:
            writer_class = WRITERS[extension]
            writer = writer_class(filename, **keywords)
            writer.set_type(extension)
        else:
            resolve_missing_extensions(extension, AVAILABLE_WRITERS)
            if to_memory:
                raise NotImplementedError(
                    MESSAGE_CANNOT_WRITE_STREAM_FORMATTER % extension)
            else:
                raise NotImplementedError(
                  MESSAGE_CANNOT_WRITE_FILE_TYPE_FORMATTER % (extension,
                                                              filename))
    return writer



def store_data(afile, data, file_type=None, **keywords):
    """Non public function to store data to afile

    :param filename: actual file name, a file stream or actual content
    :param data: the data to be written
    :param file_type: used only when filename is not a physial file name
    :param keywords: any other parameters
    """
    writer = get_writer(
        afile,
        file_type=file_type,
        **keywords)
    writer.write(data)
    writer.close()


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
    if len(list(data.keys())) == 1:
        return list(data.values())[0]
    else:
        return data
