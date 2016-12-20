"""
    pyexcel_io.sheet
    ~~~~~~~~~~~~~~~~~~~

    The io interface to file extensions

    :copyright: (c) 2014-2016 by Onni Software Ltd.
    :license: New BSD License, see LICENSE for more details
"""
from ._compact import irange
from .utils import _index_filter
import pyexcel_io.constants as constants


class NamedContent:
    """
    Helper class for content that does not have a name
    """

    def __init__(self, name, payload):
        self.name = name
        self.payload = payload


class SheetReader(object):
    """
    Generic sheet reader
    """
    def __init__(self, sheet,
                 start_row=0, row_limit=-1,
                 start_column=0, column_limit=-1,
                 skip_row_func=None, skip_column_func=None,
                 skip_empty_rows=True, row_renderer=None,
                 **keywords):
        self.native_sheet = sheet
        self.keywords = {}
        self.keywords.update(keywords)
        self.start_row = start_row
        self.row_limit = row_limit
        self.start_column = start_column
        self.column_limit = column_limit
        self.skip_row = _index_filter
        self.skip_column = _index_filter
        self.skip_empty_rows = skip_empty_rows
        self.row_renderer = row_renderer

        if skip_row_func:
            self.skip_row = skip_row_func
        if skip_column_func:
            self.skip_column = skip_column_func

    def _cell_value(self, row, column):
        """
        implement this method if the customer driver
        provides random access
        """
        raise NotImplementedError("Please implement to_array()")

    def to_array(self):
        """2 dimentional representation of the content
        """
        num_cols = self.number_of_columns()
        for row in irange(self.number_of_rows()):
            row_position = self.skip_row(row,
                                         self.start_row,
                                         self.row_limit)
            if row_position == constants.SKIP_DATA:
                continue
            elif row_position == constants.STOP_ITERATION:
                break

            return_row = []
            tmp_row = []

            for column in irange(0, num_cols):
                column_position = self.skip_column(column,
                                                   self.start_column,
                                                   self.column_limit)
                if column_position == constants.SKIP_DATA:
                    continue
                elif column_position == constants.STOP_ITERATION:
                    break

                cell_value = self._cell_value(row, column)
                tmp_row.append(cell_value)
                if cell_value is not None and cell_value != '':
                    return_row += tmp_row
                    tmp_row = []
            if self.skip_empty_rows:
                if len(return_row) < 1:
                    # we by-pass next yeild here
                    # because it is an empty row
                    continue

            if self.row_renderer:
                return_row = self.row_renderer(return_row)
            yield return_row


class SheetWriter(object):
    """
    Generic sheet writer
    """

    def __init__(self, native_book, native_sheet, name, **keywords):
        if name:
            sheet_name = name
        else:
            sheet_name = constants.DEFAULT_SHEET_NAME
        self.native_book = native_book
        self.native_sheet = native_sheet
        self.keywords = keywords
        self.set_sheet_name(sheet_name)

    def set_sheet_name(self, name):
        """
        Set sheet name
        """
        pass

    def set_size(self, size):
        """
        size of the content will be given
        """
        pass

    def write_row(self, array):
        """
        write a row into the file
        """
        raise NotImplementedError("Please implement write_row")

    def write_array(self, table):
        """
        For standalone usage, write an array
        """
        if hasattr(table, '__len__'):
            rows = len(table)
            if rows < 1:
                return
            columns = max([len(row) for row in table])
            self.set_size((rows, columns))
        for row in table:
            self.write_row(row)

    def close(self):
        """
        This call actually save the file
        """
        pass
