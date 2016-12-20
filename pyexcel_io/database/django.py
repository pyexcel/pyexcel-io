"""
    pyexcel_io.database.django
    ~~~~~~~~~~~~~~~~~~~

    The lower level handler for django import and export

    :copyright: (c) 2014-2016 by Onni Software Ltd.
    :license: New BSD License, see LICENSE for more details
"""
import logging

from pyexcel_io.book import BookReader, BookWriter
from pyexcel_io.sheet import SheetWriter
from pyexcel_io.utils import is_empty_array, swap_empty_string_for_none
import pyexcel_io.constants as constants
from pyexcel_io.database.querysets import QuerysetsReader
from ._common import TableExportAdapter, TableExporter
from ._common import TableImporter, TableImportAdapter

log = logging.getLogger(__name__)


class DjangoModelReader(QuerysetsReader):
    """Read from django model
    """
    def __init__(self, model, export_columns=None, **keywords):
        self.__model = model
        if export_columns:
            column_names = export_columns
        else:
            column_names = sorted(
                [field.attname
                 for field in self.__model._meta.concrete_fields])
        QuerysetsReader.__init__(self, self.__model.objects.all(),
                                 column_names,
                                 **keywords)


class DjangoModelWriter(SheetWriter):
    def __init__(self, adapter, batch_size=None):
        self.__batch_size = batch_size
        self.__model = adapter.model
        self.__column_names = adapter.column_names
        self.__mapdict = adapter.column_name_mapping_dict
        self.__initializer = adapter.row_initializer
        self.__objs = []

    def write_row(self, array):
        if is_empty_array(array):
            print(constants.MESSAGE_EMPTY_ARRAY)
        else:
            new_array = swap_empty_string_for_none(array)
            model_to_be_created = new_array
            if self.__initializer is not None:
                model_to_be_created = self.__initializer(new_array)
            if model_to_be_created:
                self.__objs.append(self.__model(**dict(
                    zip(self.__column_names, model_to_be_created)
                )))
            # else
                # skip the row

    def close(self):
        try:
            self.__model.objects.bulk_create(self.__objs,
                                             batch_size=self.__batch_size)
        except Exception as e:
            log.info(constants.MESSAGE_DB_EXCEPTION)
            log.info(e)
            for object in self.__objs:
                try:
                    object.save()
                except Exception as e2:
                    log.info(constants.MESSAGE_IGNORE_ROW)
                    log.info(e2)
                    log.info(object)
                    continue


class DjangoModelExportAdapter(TableExportAdapter):
    pass


class DjangoModelExporter(TableExporter):
    pass


class DjangoBookReader(BookReader):
    def open(self, file_name, **keywords):
        raise NotImplementedError()

    def open_stream(self, file_stream, **keywords):
        raise NotImplementedError()

    def open_content(self, file_content, **keywords):
        self.exporter = file_content
        self._load_from_django_models()

    def read_sheet(self, native_sheet):
        reader = DjangoModelReader(native_sheet.model,
                                   native_sheet.export_columns)
        return reader.to_array()

    def _load_from_django_models(self):
        self._native_book = self.exporter.adapters


class DjangoModelImportAdapter(TableImportAdapter):
    pass


class DjangoModelImporter(TableImporter):
    pass


class DjangoBookWriter(BookWriter):

    def open_content(self, file_content, **keywords):
        self.importer = file_content
        self._keywords = keywords

    def create_sheet(self, sheet_name):
        sheet_writer = None
        model = self.importer.get(sheet_name)
        if model:
            sheet_writer = DjangoModelWriter(
                model,
                batch_size=self._keywords.get('batch_size', None))
        return sheet_writer


_registry = {
    "file_type": constants.DB_DJANGO,
    "reader": DjangoBookReader,
    "writer": DjangoBookWriter,
    "stream_type": "special",
    "library": "built-in"
}

exports = (_registry,)
