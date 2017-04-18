"""
    pyexcel_io.database.sql
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    The lower level handler for database import and export

    :copyright: (c) 2014-2017 by Onni Software Ltd.
    :license: New BSD License, see LICENSE for more details
"""
from pyexcel_io.book import BookWriter
from pyexcel_io.sheet import SheetWriter
from pyexcel_io.utils import is_empty_array, swap_empty_string_for_none
import pyexcel_io.constants as constants
from pyexcel_io.database._common import TableImporter, TableImportAdapter


class PyexcelSQLSkipRowException(Exception):
    """
    Raised this exception to skipping a row
    while data import
    """
    pass


class SQLTableWriter(SheetWriter):
    """Write to a table
    """
    def __init__(self, session, table_params, auto_commit=True, **keywords):
        self.__session = session
        self.__table = None
        self.__initializer = None
        self.__mapdict = None
        self.__column_names = None
        self.__auto_commit = auto_commit
        self._keywords = keywords
        if len(table_params) == 4:
            (self.__table, self.__column_names,
             self.__mapdict, self.__initializer) = table_params
        else:
            raise ValueError(constants.MESSAGE_INVALID_PARAMETERS)

        if isinstance(self.__mapdict, list):
            self.__column_names = self.__mapdict
            self.__mapdict = None

    def write_row(self, array):
        if is_empty_array(array):
            print(constants.MESSAGE_EMPTY_ARRAY)
        else:
            new_array = swap_empty_string_for_none(array)
            try:
                self._write_row(new_array)
            except PyexcelSQLSkipRowException:
                print(constants.MESSAGE_IGNORE_ROW)
                print(new_array)

    def _write_row(self, array):
        row = dict(zip(self.__column_names, array))
        obj = None
        if self.__initializer:
            # allow initinalizer to return None
            # if skipping is needed
            obj = self.__initializer(row)
        if obj is None:
            obj = self.__table()
            for name in self.__column_names:
                if self.__mapdict is not None:
                    key = self.__mapdict[name]
                else:
                    key = name
                setattr(obj, key, row[name])
        self.__session.add(obj)

    def close(self):
        if self.__auto_commit:
            self.__session.commit()


class SQLTableImportAdapter(TableImportAdapter):
    def __init__(self, model):
        TableImportAdapter.__init__(self, model)
        self.table = model

    def get_name(self):
        return getattr(self.table, '__tablename__', None)


class SQLTableImporter(TableImporter):
    def __init__(self, session):
        TableImporter.__init__(self)
        self.session = session


class SQLBookWriter(BookWriter):
    file_types = [constants.DB_SQL]

    def open_content(self, file_content, auto_commit=True, **keywords):
        self.__importer = file_content
        self.__auto_commit = auto_commit

    def create_sheet(self, sheet_name):
        sheet_writer = None
        adapter = self.__importer.get(sheet_name)
        if adapter:
            sheet_writer = SQLTableWriter(
                self.__importer.session,
                (adapter.table, adapter.column_names,
                 adapter.column_name_mapping_dict,
                 adapter.row_initializer),
                auto_commit=self.__auto_commit
            )
        return sheet_writer
