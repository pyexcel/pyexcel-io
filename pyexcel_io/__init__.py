"""
    pyexcel_io
    ~~~~~~~~~~~~~~~~~~~

    Uniform interface for reading/writing different excel file formats

    :copyright: (c) 2014-2016 by Onni Software Ltd.
    :license: New BSD License, see LICENSE for more details
"""
# flake8: noqa
import logging
from ._compact import NullHandler
logging.getLogger(__name__).addHandler(NullHandler())

from .io import get_data, save_data
from pyexcel_io.manager import register_readers_and_writers
from pyexcel_io.manager import pre_register
from . import fileformat, database

exports = fileformat.exports + database.exports

from pkgutil import iter_modules

black_list = [__name__, 'pyexcel_webio', 'pyexcel_text']

for _, module_name, ispkg in iter_modules():
    if module_name in black_list:
        continue

    if ispkg and module_name.startswith('pyexcel_'):
        try:
            plugin = __import__(module_name)
            if hasattr(plugin, '__pyexcel_io_plugins__'):
                for p in plugin.__pyexcel_io_plugins__:
                    pre_register(p, module_name)
        except ImportError:
            continue

register_readers_and_writers(exports)
