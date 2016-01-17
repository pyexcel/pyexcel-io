"""
    pyexcel_io.sqlbook
    ~~~~~~~~~~~~~~~~~~~

    The lower level handler for database import and export

    :copyright: (c) 2014-2016 by Onni Software Ltd.
    :license: New BSD License, see LICENSE for more details
"""
from ._compact import OrderedDict
from .constants import (
    MESSAGE_INVALID_PARAMETERS,
    MESSAGE_EMPTY_ARRAY,
    MESSAGE_IGNORE_ROW
)
from .base import (
    BookReaderBase,
    SheetReaderBase,
    BookWriter,
    SheetWriter,
    from_query_sets,
    is_empty_array,
    swap_empty_string_for_none
)


class PyexcelSQLSkipRowException(Exception):
    """
    Raised this exception to skipping a row
    while data import
    """
    pass


class SQLTableReader(SheetReaderBase):
    """Read a table
    """
    def __init__(self, session, table):
        self.session = session
        self.table = table

    @property
    def name(self):
        return getattr(self.table, '__tablename__', None)

    def to_array(self):
        objects = self.session.query(self.table).all()
        if len(objects) == 0:
            return []
        else:
            column_names = sorted([column for column in objects[0].__dict__
                                   if column != '_sa_instance_state'])
            return from_query_sets(column_names, objects)


class SQLBookReader(BookReaderBase):
    """Read a list of tables
    """
    def __init__(self, session=None, tables=None):
        self.my_sheets = OrderedDict()
        for table in tables:
            sqltablereader = SQLTableReader(session, table)
            self.my_sheets[sqltablereader.name] = sqltablereader.to_array()

    def sheets(self):
        return self.my_sheets


class SQLTableWriter(SheetWriter):
    """Write to a table
    """
    def __init__(self, session, table_params, auto_commit=True, **keywords):
        self.session = session
        self.table = None
        self.initializer = None
        self.mapdict = None
        self.column_names = None
        self.auto_commit = auto_commit
        self.keywords = keywords
        if len(table_params) == 4:
            (self.table, self.column_names,
             self.mapdict, self.initializer) = table_params
        else:
            raise ValueError(MESSAGE_INVALID_PARAMETERS)

        if isinstance(self.mapdict, list):
            self.column_names = self.mapdict
            self.mapdict = None

    def write_row(self, array):
        if is_empty_array(array):
            print(MESSAGE_EMPTY_ARRAY)
        else:
            new_array = swap_empty_string_for_none(array)
            try:
                self._write_row(new_array)
            except PyexcelSQLSkipRowException:
                print(MESSAGE_IGNORE_ROW)
                print(new_array)

    def _write_row(self, array):
        row = dict(zip(self.column_names, array))
        obj = None
        if self.initializer:
            # allow initinalizer to return None
            # if skipping is needed
            obj = self.initializer(row)
        if obj is None:
            obj = self.table()
            for name in self.column_names:
                if self.mapdict is not None:
                    key = self.mapdict[name]
                else:
                    key = name
                setattr(obj, key, row[name])
        self.session.add(obj)

    def close(self):
        if self.auto_commit:
            self.session.commit()


class SQLBookWriter(BookWriter):
    """Write to alist of tables
    """
    def __init__(self, file, session=None, tables=None, **keywords):
        BookWriter.__init__(self, file, **keywords)
        self.session = session
        self.tables = tables

    def create_sheet(self, name):
        table_params = self.tables[name]
        return SQLTableWriter(self.session, table_params, **self.keywords)

    def close(self):
        pass
