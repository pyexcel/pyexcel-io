"""
    pyexcel_io
    ~~~~~~~~~~~~~~~~~~~

    Uniform interface for reading/writing different excel file formats

    :copyright: (c) 2014-2016 by Onni Software Ltd.
    :license: New BSD License, see LICENSE for more details
"""
from .io import get_data, save_data
from .manager import RWManager
from . import fileformat, database

exports = fileformat.exports + database.exports


try:
    import pyexcel_xls
    exports += pyexcel_xls.exports
except ImportError:
    pass


try:
    import pyexcel_xlsx
    exports += pyexcel_xlsx.exports
except ImportError:
    pass


try:
    import pyexcel_ods3
    exports += pyexcel_ods3.exports
except ImportError:
    pass


RWManager.register_readers_and_writers(exports)

