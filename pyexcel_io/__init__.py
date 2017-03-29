"""
    pyexcel_io
    ~~~~~~~~~~~~~~~~~~~

    Uniform interface for reading/writing different excel file formats

    :copyright: (c) 2014-2017 by Onni Software Ltd.
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

import pkgutil

black_list = [__name__, 'pyexcel_webio', 'pyexcel_text']

# load modules to work based with and without pyinstaller
# from: https://github.com/webcomics/dosage/blob/master/dosagelib/loader.py
# see: https://github.com/pyinstaller/pyinstaller/issues/1905
# load modules using iter_modules()
# (should find all plug ins in normal build, but not pyinstaller)

prefix = 'pyexcel_'

module_names = [m[1] for m in pkgutil.iter_modules()
                if m[2] and m[1].startswith(prefix)]

# special handling for PyInstaller
toc = set()
for t in (i.toc for i in map(pkgutil.get_importer, __path__)
          if hasattr(i, 'toc')):
    toc |= t

for elm in toc:
    if elm.startswith(prefix) and '.' not in elm:
        module_names.append(elm)

# loop through modules and find our plug ins
for module_name in module_names:

    if module_name in black_list:
        continue

    try:
        plugin = __import__(module_name)
        if hasattr(plugin, '__pyexcel_io_plugins__'):
            for p in plugin.__pyexcel_io_plugins__:
                pre_register(p, module_name)
    except ImportError:
        continue

register_readers_and_writers(exports)
