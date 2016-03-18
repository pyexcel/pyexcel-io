from .constants import (
    MESSAGE_LOADING_FORMATTER,
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

from .csvbook import CSVBookReader, CSVBookWriter, TSVBookReader, TSVBookWriter
from .csvzipbook import CSVZipBookReader, TSVZipBookReader
from .csvzipbook import CSVZipBookWriter, TSVZipBookWriter

from .base import Reader, Writer
from .djangobook import DjangoBookReader,  DjangoBookWriter
from .sqlbook import SQLBookReader, SQLBookWriter


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


from ._compact import is_string


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
        FILE_FORMAT_TSV: TSVBookReader,
        FILE_FORMAT_CSVZ: CSVZipBookReader,
        FILE_FORMAT_TSVZ: TSVZipBookReader,
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
            if file_type in [FILE_FORMAT_CSV, FILE_FORMAT_TSV, FILE_FORMAT_CSVZ, FILE_FORMAT_TSVZ, DB_DJANGO, DB_SQL, FILE_FORMAT_XLS]:
                return reader_class()
            else:
                return Reader(file_type, reader_class)
        else:
            resolve_missing_extensions(file_type, AVAILABLE_READERS)


class WriterFactory(object):
    factories = {
        FILE_FORMAT_CSV: CSVBookWriter,
        FILE_FORMAT_TSV: TSVBookWriter,
        FILE_FORMAT_CSVZ: CSVZipBookWriter,
        FILE_FORMAT_TSVZ: TSVZipBookWriter,
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
            if file_type in [FILE_FORMAT_CSV, FILE_FORMAT_TSVZ, FILE_FORMAT_CSVZ, DB_DJANGO, DB_SQL, FILE_FORMAT_XLS]:
                return writer_class()
            else:
                return Writer(file_type, writer_class)
        else:
            resolve_missing_extensions(file_type, AVAILABLE_WRITERS)
