"""
    pyexcel_io._compact
    ~~~~~~~~~~~~~~~~~~~

    Compatibles

    :copyright: (c) 2014-2016 by Onni Software Ltd.
    :license: New BSD License, see LICENSE for more details
"""
# flake8: noqa
import types
import sys

PY2 = sys.version_info[0] == 2
PY26 = PY2 and sys.version_info[1] < 7

if PY26:
    from ordereddict import OrderedDict
else:
    from collections import OrderedDict

def is_generator(struct):
    return isinstance(struct, types.GeneratorType)


if PY2:
    from StringIO import StringIO
    from StringIO import StringIO as BytesIO
    text_type = unicode
    irange = xrange

    class Iterator(object):
        def next(self):
            return type(self).__next__(self)

else:
    from io import StringIO, BytesIO
    text_type = str
    Iterator = object
    irange = range

def isstream(instance):
    return hasattr(instance, 'read')


def is_string(atype):
    """find out if a type is str or not"""
    if atype == str:
        return True
    elif PY2:
        if atype == unicode:
            return True
    return False
