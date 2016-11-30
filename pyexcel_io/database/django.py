"""
    pyexcel_io.database.django
    ~~~~~~~~~~~~~~~~~~~

    The lower level handler for django import and export

    :copyright: (c) 2014-2016 by Onni Software Ltd.
    :license: New BSD License, see LICENSE for more details
"""
from pyexcel_io.book import BookReader, BookWriter
from pyexcel_io.sheet import SheetWriter
from pyexcel_io.utils import is_empty_array, swap_empty_string_for_none
import pyexcel_io.constants as constants
from pyexcel_io.database.querysets import QuerysetsReader
from ._common import TableExportAdapter, TableExporter
from ._common import TableImporter, TableImportAdapter


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
    def __init__(self, model, batch_size=None):
        self.batch_size = batch_size
        self.mymodel = None
        self.column_names = None
        self.mapdict = None
        self.initializer = None

        self.mymodel, self.column_names, self.mapdict, self.initializer = model

        if self.initializer is None:
            self.initializer = lambda row: row
        if isinstance(self.mapdict, list):
            self.column_names = self.mapdict
            self.mapdict = None
        elif isinstance(self.mapdict, dict):
            self.column_names = [self.mapdict[name]
                                 for name in self.column_names]
        self.objs = []

    def write_row(self, array):
        if is_empty_array(array):
            print(constants.MESSAGE_EMPTY_ARRAY)
        else:
            new_array = swap_empty_string_for_none(array)
            model_to_be_created = new_array
            if self.initializer is not None:
                model_to_be_created = self.initializer(new_array)
            if model_to_be_created:
                self.objs.append(self.mymodel(**dict(
                    zip(self.column_names, model_to_be_created)
                )))
            # else
                # skip the row

    def close(self):
        try:
            self.mymodel.objects.bulk_create(self.objs,
                                             batch_size=self.batch_size)
        except Exception as e:
            print(constants.MESSAGE_DB_EXCEPTION)
            print(e)
            for object in self.objs:
                try:
                    object.save()
                except Exception as e2:
                    print(constants.MESSAGE_IGNORE_ROW)
                    print(e2)
                    print(object)
                    continue


class DjangoModelWriterNew(DjangoModelWriter):
    def __init__(self, adapter, batch_size=None):
        self.batch_size = batch_size
        self.mymodel = adapter.model
        self.column_names = adapter.column_names
        self.mapdict = adapter.column_name_mapping_dict
        self.initializer = adapter.row_initializer
        self.objs = []


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

    def create_sheet(self, sheet_name):
        sheet_writer = None
        model = self.importer.get(sheet_name)
        if model:
            sheet_writer = DjangoModelWriterNew(model)
        return sheet_writer


_registry = {
    "file_type": constants.DB_DJANGO,
    "reader": DjangoBookReader,
    "writer": DjangoBookWriter,
    "stream_type": "special",
    "library": "built-in"
}

exports = (_registry,)
