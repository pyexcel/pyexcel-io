from functools import partial

from .constants import (
    MESSAGE_LOADING_FORMATTER,
    MESSAGE_ERROR_03,
    MESSAGE_WRONG_IO_INSTANCE,
    FILE_FORMAT_CSV,
    FILE_FORMAT_TSV,
    FILE_FORMAT_CSVZ,
    FILE_FORMAT_TSVZ,
    FILE_FORMAT_ODS,
    FILE_FORMAT_XLS,
    FILE_FORMAT_XLSX,
    FILE_FORMAT_XLSM,
    DB_SQL,
    DB_DJANGO
)

from .csvbook import CSVBook, CSVWriter
from .csvzipbook import CSVZipWriter, CSVZipBook
from .sqlbook import SQLBookReader, SQLBookWriter
from .djangobook import DjangoBookReader, DjangoBookWriter
from .newbase import CSVBookReader, Reader, validate_io


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


from ._compact import (
    is_string, BytesIO, StringIO,
    isstream, PY2)


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


class ReaderFactory(object):
    factories = {
        FILE_FORMAT_CSV: CSVBookReader,
        FILE_FORMAT_TSV: partial(CSVBook, dialect="excel-tab"),
        FILE_FORMAT_CSVZ: CSVZipBook,
        FILE_FORMAT_TSVZ: partial(CSVZipBook, dialect="excel-tab"),
        DB_SQL: SQLBookReader,
        DB_DJANGO: DjangoBookReader
    }

    @staticmethod
    def add_factory(file_type, reader_class):
        ReaderFactory.factories[file_type] = reader_class

    @staticmethod
    def create_reader(file_type):
        if file_type in ReaderFactory.factories:
            reader_class = ReaderFactory.factories[file_type]
            if file_type == FILE_FORMAT_CSV:
                return reader_class(file_type)
            else:
                return Reader(file_type, reader_class)
        else:
            resolve_missing_extensions(file_type, AVAILABLE_READERS)


class WriterFactory(object):
    factories = {
        FILE_FORMAT_CSV: CSVWriter,
        FILE_FORMAT_TSV: partial(CSVWriter, dialect="excel-tab"),
        FILE_FORMAT_CSVZ: CSVZipWriter,
        FILE_FORMAT_TSVZ: partial(CSVZipWriter, dialect="excel-tab"),
        DB_SQL: SQLBookWriter,
        DB_DJANGO: DjangoBookWriter
    }
    @staticmethod
    def add_factory(file_type, writer_class):
        WriterFactory.factories[file_type] = writer_class

    @staticmethod
    def create_writer(file_type):
        if file_type in WriterFactory.factories:
            writer_class = WriterFactory.factories[file_type]
            return Writer(file_type, writer_class)
        else:
            resolve_missing_extensions(file_type, AVAILABLE_WRITERS)


class Writer(object):
    def __init__(self, file_type, writer_class):
        self.file_type = file_type
        self.writer_class = writer_class
        self.writer = None
        self.file_alike_object = None

    def open(self, file_name, **keywords):
        self.file_alike_object = file_name
        self.writing_keywords = keywords

    def open_stream(self, file_stream, **keywords):
        if isstream(file_stream):
            if not validate_io(self.file_type, file_stream):
                raise IOError(MESSAGE_WRONG_IO_INSTANCE)
        else:
            raise IOError(MESSAGE_ERROR_03)
        self.open(file_stream, **keywords)

    def write(self, data):
        self.writer = self.writer_class(self.file_alike_object,
                                        **self.writing_keywords)
        self.writer.write(data)

    def close(self):
        if self.writer:
            self.writer.close()
