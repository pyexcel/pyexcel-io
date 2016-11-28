"""
    pyexcel_io.manager
    ~~~~~~~~~~~~~~~~~~~

    factory for getting readers and writers

    :copyright: (c) 2014-2016 by Onni Software Ltd.
    :license: New BSD License, see LICENSE for more details
"""
from pyexcel_io._compact import StringIO, BytesIO
import pyexcel_io.utils as utils


reader_factories = {}
writer_factories = {}
text_stream_types = []
binary_stream_types = []
file_types = ()
mime_types = {}


def get_writers():
    return writer_factories.keys()


def register_readers_and_writers(plugins):
    for plugin in plugins:
        the_file_type = plugin['file_type']
        register_a_file_type(
            the_file_type, plugin.get('stream_type', None),
            plugin.get('mime_type', None))
        if 'reader' in plugin:
            _register_a_reader(
                the_file_type, plugin['reader'], plugin['library'])
        if 'writer' in plugin:
            _register_a_writer(
                the_file_type, plugin['writer'], plugin['library'])
        # else:
            # ignored for now


def register_a_file_type(file_type, stream_type, mime_type):
    global file_types
    file_types += (file_type,)
    stream_type = stream_type
    if stream_type == 'text':
        register_file_type_as_text_stream(file_type)
    elif stream_type == 'binary':
        register_file_type_as_binary_stream(file_type)
    if mime_type is not None:
        mime_types[file_type] = mime_type


def register_file_type_as_text_stream(file_type):
    text_stream_types.append(file_type)


def register_file_type_as_binary_stream(file_type):
    binary_stream_types.append(file_type)


def get_io(file_type):
    """A utility function to help you generate a correct io stream

    :param file_type: a supported file type
    :returns: a appropriate io stream, None otherwise
    """
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
    __file_type = file_type.lower()
    
    if __file_type in text_stream_types:
        return "string"
    elif __file_type in binary_stream_types:
        return "bytes"
    else:
        return None


def _register_a_reader(file_type, reader_class, library):
    _add_a_handler(reader_factories,
                   file_type, reader_class, library)


def _register_a_writer(file_type, writer_class, library):
    _add_a_handler(writer_factories,
                   file_type, writer_class, library)


def _add_a_handler(factories, file_type, handler, library):
    if file_type not in factories:
        factories[file_type] = {}
    factories[file_type][library] = handler


def create_reader(file_type, library=None):
    reader = _get_a_handler(
        reader_factories, file_type, library)
    if reader is None:
        utils.resolve_missing_readers(file_type)
    return reader


def create_writer(file_type, library=None):
    writer = _get_a_handler(
        writer_factories, file_type, library)
    if writer is None:
        utils.resolve_missing_writers(file_type)
    return writer


def _get_a_handler(factories, file_type, library):
    if file_type in factories:
        handler_dict = factories[file_type.lower()]
        if library is not None:
            handler_class = handler_dict.get(library, None)
            if handler_class is None:
                raise Exception("%s is not installed" % library)
        else:
            for _, _handler in handler_dict.items():
                handler_class = _handler
                break
        handler = handler_class()
        handler.set_type(file_type)
        return handler

    raise IOError("No suitable library found for %s" % file_type)
