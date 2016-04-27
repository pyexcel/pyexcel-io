"""
    pyexcel_io.base
    ~~~~~~~~~~~~~~~~~~~

    The io interface to file extensions

    :copyright: (c) 2014-2016 by Onni Software Ltd.
    :license: New BSD License, see LICENSE for more details
"""
from ._compact import StringIO, BytesIO
from .utils import resolve_missing_readers, resolve_missing_writers


class RWManager(object):
    reader_factories = {}
    writer_factories = {}
    text_stream_types = []
    binary_stream_types = []
    file_types = []

    @staticmethod
    def register_readers_and_writers(plugins):
        for plugin in plugins:
            RWManager.file_types.append(plugin['file_type'])
            if 'reader' in plugin:
                RWManager.register_a_reader(plugin['file_type'], plugin['reader'])
            if 'writer' in plugin:
                RWManager.register_a_writer(plugin['file_type'], plugin['writer'])
            stream_type = plugin.get('stream_type', None)
            if stream_type == 'text':
                RWManager.register_file_type_as_text_stream(plugin['file_type'])
            elif stream_type == 'binary':
                RWManager.register_file_type_as_binary_stream(plugin['file_type'])
            #else:
                # ignored for now

    @staticmethod
    def register_file_type_as_text_stream(file_type):
        RWManager.text_stream_types.append(file_type)

    @staticmethod
    def register_file_type_as_binary_stream(file_type):
        RWManager.binary_stream_types.append(file_type)


    @staticmethod
    def register_readers(file_type_reader_dict):
        for file_type, reader_class in file_type_reader_dict.items():
            RWManager.register_a_reader(file_type, reader_class)

    @staticmethod
    def register_a_reader(file_type, reader_class):
        RWManager._add_a_handler(RWManager.reader_factories,
                                 file_type, reader_class)

    @staticmethod
    def register_writers(file_type_writer_dict):
        for file_type, writer_class in file_type_writer_dict.items():
            RWManager.register_a_writer(file_type, writer_class)

    @staticmethod
    def register_a_writer(file_type, writer_class):
        RWManager._add_a_handler(RWManager.writer_factories,
                                 file_type, writer_class)

    @staticmethod
    def _add_a_handler(factories, file_type, handler):
        factories[file_type] = handler

    @staticmethod
    def create_reader(file_type):
        if file_type in RWManager.reader_factories:
            reader_class = RWManager.reader_factories[file_type]
            reader = reader_class()
            reader.set_type(file_type)
            return reader
        else:
            resolve_missing_readers(file_type)

    @staticmethod
    def create_writer(file_type):
        if file_type in RWManager.writer_factories:
            writer_class = RWManager.writer_factories[file_type]
            writer = writer_class()
            writer.set_type(file_type)
            return writer
        else:
            resolve_missing_writers(file_type)


    @staticmethod
    def get_io(file_type):
        """A utility function to help you generate a correct io stream
    
        :param file_type: a supported file type
        :returns: a appropriate io stream, None otherwise
        """
        if file_type in RWManager.text_stream_types:
            return StringIO()
        elif file_type in RWManager.binary_stream_types:
            return BytesIO()
        else:
            return None
    
    
    @staticmethod
    def validate_io(file_type, stream):
        if file_type in RWManager.text_stream_types:
            return isinstance(stream, StringIO)
        elif file_type in RWManager.binary_stream_types:
            return isinstance(stream, BytesIO)
        else:
            return False
