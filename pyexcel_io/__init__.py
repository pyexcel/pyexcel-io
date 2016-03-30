"""
    pyexcel_io
    ~~~~~~~~~~~~~~~~~~~

    Uniform interface for reading/writing different excel file formats

    :copyright: (c) 2014-2016 by Onni Software Ltd.
    :license: New BSD License, see LICENSE for more details
"""
from .io import get_data, save_data
from .manager import RWManager


try:
    import pyexcel_xls
    pyexcel_xls.extend_pyexcel(RWManager)
except ImportError:
    pass


try:
    import pyexcel_xlsx
    pyexcel_xlsx.extend_pyexcel(RWManager)
except ImportError:
    pass


try:
    import pyexcel_ods3
    pyexcel_ods3.extend_pyexcel(RWManager)
except ImportError:
    pass

