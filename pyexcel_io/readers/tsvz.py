"""
    pyexcel_io.fileformat.tsvz
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    The lower level tsvz file format handler.

    :copyright: (c) 2014-2020 by Onni Software Ltd.
    :license: New BSD License, see LICENSE for more details
"""
from pyexcel_io.constants import KEYWORD_TSV_DIALECT

from .csvz import FileReader


class TSVZipFileReader(FileReader):
    """ read zipped tab separated value file

    it supports single tsv file and mulitple tsv files
    """

    def open(self, file_name, **keywords):
        keywords["dialect"] = KEYWORD_TSV_DIALECT
        super(TSVZipFileReader, self).open(file_name, **keywords)
