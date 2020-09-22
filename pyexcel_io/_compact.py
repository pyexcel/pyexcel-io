"""
    pyexcel_io._compact
    ~~~~~~~~~~~~~~~~~~~

    Compatibles

    :copyright: (c) 2014-2020 by Onni Software Ltd.
    :license: New BSD License, see LICENSE for more details
"""
# flake8: noqa
# pylint: disable=import-error
# pylint: disable=invalid-name
# pylint: disable=too-few-public-methods
# pylint: disable=ungrouped-imports
# pylint: disable=redefined-variable-type
import sys
import types
import logging
from collections import OrderedDict

try:
    from logging import NullHandler
except ImportError:

    class NullHandler(logging.Handler):
        def emit(self, record):
            pass


from io import BytesIO, StringIO

text_type = str
Iterator = object
irange = range


def isstream(instance):
    """ check if a instance is a stream """
    try:
        import mmap

        i_am_not_mmap_obj = not isinstance(instance, mmap.mmap)
    except ImportError:
        # Python 2.6 or Google App Engine
        i_am_not_mmap_obj = True

    return hasattr(instance, "read") and i_am_not_mmap_obj


def is_string(atype):
    """find out if a type is str or not"""
    if atype == str:
        return True

    elif PY2:
        if atype == unicode:
            return True

    return False
