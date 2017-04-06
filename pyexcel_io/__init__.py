"""
    pyexcel_io
    ~~~~~~~~~~~~~~~~~~~

    Uniform interface for reading/writing different excel file formats

    :copyright: (c) 2014-2017 by Onni Software Ltd.
    :license: New BSD License, see LICENSE for more details
"""
import logging
from ._compact import NullHandler
logging.getLogger(__name__).addHandler(NullHandler())  # noqa

from .io import get_data, save_data  # noqa
from pyexcel_io.plugins import load_plugins


black_list = [__name__, 'pyexcel_webio', 'pyexcel_text']
white_list = ['pyexcel_io.fileformat', 'pyexcel_io.database']
prefix = 'pyexcel_'

load_plugins(prefix, __path__, black_list, white_list)
