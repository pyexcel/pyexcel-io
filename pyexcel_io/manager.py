"""
    pyexcel_io.manager
    ~~~~~~~~~~~~~~~~~~~

    Control file streams

    :copyright: (c) 2014-2017 by Onni Software Ltd.
    :license: New BSD License, see LICENSE for more details
"""
from pyexcel_io._compact import StringIO, BytesIO


mime_types = {}
file_types = ()
text_stream_types = []
binary_stream_types = []


def register_stream_type(file_type, stream_type):
    if stream_type == 'text':
        text_stream_types.append(file_type)
    elif stream_type == 'binary':
        binary_stream_types.append(file_type)


def get_io(file_type):
    """A utility function to help you generate a correct io stream

    :param file_type: a supported file type
    :returns: a appropriate io stream, None otherwise
    """
    __file_type = None
    if file_type:
        __file_type = file_type.lower()

    if __file_type in text_stream_types:
        return StringIO()
    elif __file_type in binary_stream_types:
        return BytesIO()
    else:
        return None


def get_io_type(file_type):
    """A utility function to help you generate a correct io stream

    :param file_type: a supported file type
    :returns: a appropriate io stream, None otherwise
    """
    __file_type = None
    if file_type:
        __file_type = file_type.lower()

    if __file_type in text_stream_types:
        return "string"
    elif __file_type in binary_stream_types:
        return "bytes"
    else:
        return None


def register_a_file_type(file_type, stream_type, mime_type):
    global file_types
    file_types += (file_type,)
    stream_type = stream_type
    if mime_type is not None:
        mime_types[file_type] = mime_type
    register_stream_type(file_type, stream_type)
