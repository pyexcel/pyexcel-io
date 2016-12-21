from pyexcel_io.sheet import SheetReader
import pyexcel_io.utils as utils
from itertools import chain


class QuerysetsReader(SheetReader):

    def __init__(self, query_sets, column_names, **keywords):
        SheetReader.__init__(self, query_sets, **keywords)
        self.__column_names = column_names
        self.__query_sets = query_sets

    def to_array(self):
        """
        Convert query sets into an array
        """
        if len(self.__query_sets) == 0:
            yield []
        for element in SheetReader.to_array(self):
            yield element

    def row_iterator(self):
        return chain([self.__column_names],
                     self.__query_sets)

    def column_iterator(self, row):
        if self.__column_names is not None:
            if isinstance(row, list):
                for element in row:
                    yield element
            else:
                for column in self.__column_names:
                    if '__' in column:
                        value = utils._get_complex_attribute(
                            row, column)
                    else:
                        value = utils._get_simple_attribute(
                            row, column)
                    yield value
