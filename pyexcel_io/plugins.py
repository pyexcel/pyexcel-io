"""
    pyexcel_io.plugins
    ~~~~~~~~~~~~~~~~~~~

    factory for getting readers and writers

    :copyright: (c) 2014-2017 by Onni Software Ltd.
    :license: New BSD License, see LICENSE for more details
"""
import logging
from collections import defaultdict

from lml.plugin import scan_plugins
from lml.manager import PluginManager

import pyexcel_io.utils as ioutils
import pyexcel_io.manager as manager
import pyexcel_io.exceptions as exceptions
import pyexcel_io.constants as constants


log = logging.getLogger(__name__)
ERROR_MESSAGE_FORMATTER = "one of these plugins for %s data in '%s': %s"
UPGRADE_MESSAGE = "Please upgrade the plugin '%s' according to \
plugin compactibility table."


class IOManager(PluginManager):
    def __init__(self):
        PluginManager.__init__(self, 'pyexcel io plugin')
        self.registry = defaultdict(list)
        self.text_stream_types = []
        self.binary_stream_types = []
        self.loaded_reader_registry = defaultdict(dict)
        self.loaded_writer_registry = defaultdict(dict)

    def load_me_later(self, plugin_meta, module_name):
        PluginManager.load_me_later(self, plugin_meta, module_name)
        if not isinstance(plugin_meta, dict):
            plugin = module_name.replace('_', '-')
            raise exceptions.UpgradePlugin(UPGRADE_MESSAGE % plugin)
        library_import_path = "%s.%s" % (module_name, plugin_meta['submodule'])
        for file_type in plugin_meta['file_types']:
            self.registry[file_type].append(
                (library_import_path, plugin_meta['submodule']))
            manager.register_stream_type(file_type, plugin_meta['stream_type'])

    def load_me_now(self, key, **keywords):
        PluginManager.load_me_now(self, key, **keywords)
        __key = key.lower()
        if __key in self.registry:
            for path in self.registry[__key]:
                self.dynamic_load_library(path)
            # once loaded, forgot it
            self.registry.pop(__key)

    def dynamic_load_library(self, library_import_path):
        plugin = PluginManager.dynamic_load_library(self, library_import_path)
        register_readers_and_writers(plugin.exports)
        return plugin

    def register_a_plugin(self, action, file_type, plugin, library):
        registry = self.loaded_reader_registry
        if action == 'write':
            registry = self.loaded_writer_registry

        registry[file_type][library] = plugin

    def get_a_plugin(self, action, file_type, library):
        __file_type = file_type.lower()
        registry = self.loaded_reader_registry
        known_plugins = ioutils.AVAILABLE_READERS
        if action == 'write':
            registry = self.loaded_writer_registry
            known_plugins = ioutils.AVAILABLE_WRITERS

        self.load_me_now(__file_type)
        if __file_type in registry:
            handler_dict = registry[__file_type]
            if library is not None:
                handler_cls = handler_dict.get(library, None)
                if handler_cls is None:
                    raise Exception("%s is not installed" % library)
            else:
                for _, _handler in handler_dict.items():
                    handler_cls = _handler
                    break
            handler = handler_cls()
            handler.set_type(__file_type)
            return handler
        plugins = known_plugins.get(file_type, None)
        if plugins:
            message = "Please install "
            if len(plugins) > 1:
                message += ERROR_MESSAGE_FORMATTER % (
                    action, file_type, ','.join(plugins))
            else:
                message += plugins[0]
            raise exceptions.SupportingPluginAvailableButNotInstalled(message)
        else:
            raise exceptions.NoSupportingPluginFound(
                "No suitable library found for %s" % file_type)

    def get_all_reader_formats(self):
        all_formats = set(list(self.loaded_reader_registry.keys()) +
                          list(ioutils.AVAILABLE_READERS.keys()))
        all_formats = all_formats.difference(set([constants.DB_SQL,
                                                  constants.DB_DJANGO]))
        return all_formats

    def get_all_writer_formats(self):
        all_formats = set(list(self.loaded_writer_registry.keys()) +
                          list(ioutils.AVAILABLE_WRITERS.keys()))
        all_formats = all_formats.difference(set([constants.DB_SQL,
                                                  constants.DB_DJANGO]))
        return all_formats


iomanager = IOManager()


def register_readers_and_writers(plugins):
    __debug_writer_file_types = []
    __debug_reader_file_types = []
    for plugin in plugins:
        the_file_type = plugin['file_type']
        manager.register_a_file_type(
            the_file_type, plugin.get('stream_type', None),
            plugin.get('mime_type', None))
        if 'reader' in plugin:
            iomanager.register_a_plugin(
                'read', the_file_type, plugin['reader'], plugin['library'])
            __debug_reader_file_types.append(plugin['file_type'])
        if 'writer' in plugin:
            iomanager.register_a_plugin(
                'write', the_file_type, plugin['writer'], plugin['library'])
            __debug_writer_file_types.append(plugin['file_type'])
        # else:
            # ignored for now
    log.debug("imported writers for:" + ",".join(__debug_writer_file_types))
    log.debug("imported readers for:" + ",".join(__debug_reader_file_types))


def load_plugins(prefix, path, black_list, white_list):
    scan_plugins(
        prefix, constants.DEFAULT_PLUGIN_NAME,
        path, black_list, white_list)
