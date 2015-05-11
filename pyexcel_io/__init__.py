"""
    pyexcel.io
    ~~~~~~~~~~~~~~~~~~~

    Uniform interface for reading/writing different excel file formats

    :copyright: (c) 2014-2015 by Onni Software Ltd.
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
    BookWriter
)
from .csvbook import CSVBook, CSVWriter
from .csvzipbook import CSVZipWriter, CSVZipBook
from .sqlbook import SQLBookReader, SQLBookWriter
from .djangobook import DjangoBookReader, DjangoBookWriter
from ._compact import is_string, BytesIO, StringIO, isstream, OrderedDict, PY2
from .constants import (
    MESSAGE_LOADING_FORMATTER,
    MESSAGE_ERROR_03,
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
)


# A list of registered readers
READERS = {
    FILE_FORMAT_CSV: CSVBook,
    FILE_FORMAT_TSV: partial(CSVBook, dialect="excel-tab"),
    FILE_FORMAT_CSVZ: CSVZipBook,
    FILE_FORMAT_TSVZ: partial(CSVZipBook, dialect="excel-tab"),
    DB_SQL: SQLBookReader,
    DB_DJANGO: DjangoBookReader
}

AVAILABLE_READERS = {
    FILE_FORMAT_XLS: 'pyexcel-xls',
    FILE_FORMAT_XLSX: ('pyexcel-xls', 'pyexcel-xlsx'),
    FILE_FORMAT_XLSM: ('pyexcel-xls', 'pyexcel-xlsx'),
    FILE_FORMAT_ODS: ('pyexcel-ods', 'pyexcel-ods3')
}

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

def list_readers():
    """list available readers"""
    print(READERS.keys())


def list_writers():
    """list available writers"""
    print(WRITERS.keys())


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

def load_data(filename,
              file_type=None,
              sheet_name=None,
              sheet_index=None,
              **keywords):
    """Load data from any supported excel formats

    Tests:

        >>> import pyexcel as pe
        >>> pe.load("test.strange_type")
        Traceback (most recent call last):
            ...
        NotImplementedError: Cannot read content of file type strange_type from file test.strange_type
        >>> pe.load(("strange_type", "fake io"))
        Traceback (most recent call last):
            ...
        NotImplementedError: Cannot read content of file type strange_type from stream
        >>> pe.load("test.ods")
        Traceback (most recent call last):
            ...
        NotImplementedError: The plugin for file type ods is not installed. Please install pyexcel-ods or pyexcel-ods3
        >>> pe.load(("ods", "fake io"))
        Traceback (most recent call last):
            ...
        NotImplementedError: The plugin for file type ods is not installed. Please install pyexcel-ods or pyexcel-ods3
    
    """
    extension = None
    book = None
    from_memory = False
    content = None
    if filename in READERS:
        book_class = READERS[filename]
        book = book_class(**keywords)
    else:
        if file_type is not None:
            from_memory = True
            extension = file_type
        elif is_string(type(filename)):
            extension = filename.split(".")[-1]
        else:
            raise IOError(MESSAGE_ERROR_03)
        if extension in READERS:
            book_class = READERS[extension]
            if from_memory:
                if isstream(filename):
                    content = filename
                else:
                    io = get_io(file_type)
                    io.write(filename)
                    io.seek(0)
                    content = io
                book = book_class(None, file_content=content,
                                  load_sheet_with_name=sheet_name,
                                  load_sheet_at_index=sheet_index,
                                  **keywords)
            else:
                book = book_class(filename,
                                  load_sheet_with_name=sheet_name,
                                  load_sheet_at_index=sheet_index,
                                  **keywords)
        else:
            resolve_missing_extensions(extension, AVAILABLE_READERS)
            if from_memory:
                raise NotImplementedError(MESSAGE_CANNOT_READ_STREAM_FORMATTER % extension)
            else:
                raise NotImplementedError(MESSAGE_CANNOT_READ_FILE_TYPE_FORMATTER% (extension, filename))
    return book.sheets()


def get_writer(filename, file_type=None, **keywords):
    """Create a writer from any supported excel formats

    Tests:

        >>> import pyexcel as pe
        >>> data = [[1,2]]
        >>> sheet = pe.Sheet(data)
        >>> sheet.save_as("test.strange_type")
        Traceback (most recent call last):
            ...
        NotImplementedError: Cannot write content of file type strange_type to file test.strange_type
        >>> sheet.save_to_memory("strange_type", "fake io")
        Traceback (most recent call last):
            ...
        IOError: cannot handle unknown content
        >>> sheet.save_as("test.ods")
        Traceback (most recent call last):
            ...
        NotImplementedError: The plugin for file type ods is not installed. Please install pyexcel-ods or pyexcel-ods3
        >>> sheet.save_to_memory("ods", "fake io")
        Traceback (most recent call last):
            ...
        IOError: cannot handle unknown content
        
    """
    extension = None
    writer = None
    to_memory = False
    if filename in WRITERS:
        writer_class = WRITERS[filename]
        writer = writer_class(filename, **keywords)
    else:
        if file_type is not None:
            if isstream(filename):
                extension = file_type
                to_memory = True
            else:
                raise IOError(MESSAGE_ERROR_03)
        elif is_string(type(filename)):
            extension = filename.split(".")[-1]
        else:
            raise IOError(MESSAGE_ERROR_03)
        if extension in WRITERS:
            writer_class = WRITERS[extension]
            writer = writer_class(filename, **keywords)
        else:
            resolve_missing_extensions(extension, AVAILABLE_WRITERS)
            if to_memory:
                raise NotImplementedError(MESSAGE_CANNOT_WRITE_STREAM_FORMATTER % extension)
            else:
                raise NotImplementedError(MESSAGE_CANNOT_WRITE_FILE_TYPE_FORMATTER % (extension, filename))
    return writer


def get_io(file_type):
    if file_type in [FILE_FORMAT_CSV, FILE_FORMAT_TSV]:
        return StringIO()
    elif file_type in [FILE_FORMAT_CSVZ, FILE_FORMAT_TSVZ, FILE_FORMAT_ODS, FILE_FORMAT_XLS, FILE_FORMAT_XLSX, FILE_FORMAT_XLSM]:
        return BytesIO()
    else:
        return None


def save_data(afile, data, file_type=None, **keywords):
    to_store = data
    if isinstance(data, list):
        single_sheet_in_book = True
        to_store = {"csv": data}
    else:
        single_sheet_in_book = False

    if isstream(afile):
        file_type = FILE_FORMAT_CSV

    writer = get_writer(
        afile,
        file_type=file_type,
        single_sheet_in_book=single_sheet_in_book,
        **keywords)
    writer.write(to_store)
    writer.close()


def get_data(afile, file_type=None, **keywords):
    if isstream(afile) and file_type is None:
        file_type='csv'
    data = load_data(afile, file_type=file_type, **keywords)
    if len(list(data.keys())) == 1:
        return list(data.values())[0]
    else:
        return data
