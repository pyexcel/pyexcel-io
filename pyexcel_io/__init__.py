"""
    pyexcel_io
    ~~~~~~~~~~~~~~~~~~~

    Uniform interface for reading/writing different excel file formats

    :copyright: (c) 2014-2016 by Onni Software Ltd.
    :license: New BSD License, see LICENSE for more details
"""
from .fileformat import csvformat
from .fileformat import csvz
from .fileformat import tsv
from .fileformat import tsvz
from .database import django
from .database import sql
from .io import get_data, save_data
from .manager import RWManager


try:
    import pyexcel_xls
except ImportError:
    pass


try:
    import pyexcel_xlsx
except ImportError:
    pass


try:
    import pyexcel_ods3
except ImportError:
    pass

