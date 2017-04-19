"""
    pyexcel_io.plugins
    ~~~~~~~~~~~~~~~~~~~

    factory for getting readers and writers

    :copyright: (c) 2014-2017 by Onni Software Ltd.
    :license: New BSD License, see LICENSE for more details
"""
from collections import defaultdict

from lml.plugin import scan_plugins
from lml.manager import PluginManager, PluginList, PluginInfo

import pyexcel_io.utils as ioutils
import pyexcel_io.manager as manager
import pyexcel_io.exceptions as exceptions
import pyexcel_io.constants as constants


ERROR_MESSAGE_FORMATTER = "one of these plugins for %s data in '%s': %s"
UPGRADE_MESSAGE = "Please upgrade the plugin '%s' according to \
plugin compactibility table."
READER_PLUGIN = 'pyexcel-io reader'
WRITER_PLUGIN = 'pyexcel-io writer'


class IORegistry(PluginList):
    def add_a_reader(self, submodule=None, file_types=None, stream_type=None):
        return self.add_a_plugin(READER_PLUGIN, submodule,
                                 file_types, stream_type)

    def add_a_writer(self, submodule=None, file_types=None, stream_type=None):
        return self.add_a_plugin(WRITER_PLUGIN, submodule,
                                 file_types, stream_type)


class IOManager(PluginManager):
    def __init__(self, plugin_type, known_list):
        PluginManager.__init__(self, plugin_type)
        self.loaded_registry = defaultdict(dict)
        self.known_plugins = known_list

    def load_me_later(self, plugin_info, module_name):
        PluginManager.load_me_later(self, plugin_info, module_name)
        if not isinstance(plugin_info, PluginInfo):
            pypi_name = _get_me_pypi_package_name(module_name)
            raise exceptions.UpgradePlugin(UPGRADE_MESSAGE % pypi_name)
        library_import_path = "%s.%s" % (module_name, plugin_info.submodule)
        for file_type in plugin_info.file_types:
            self.registry[file_type].append(
                (library_import_path, plugin_info.submodule))
            manager.register_stream_type(file_type, plugin_info.stream_type)

    def load_me_now(self, key, **keywords):
        PluginManager.load_me_now(self, key, **keywords)
        __key = key.lower()
        if __key in self.registry:
            for path in self.registry[__key]:
                self.dynamic_load_library(path)
            # once loaded, forgot it
            self.registry.pop(__key)

    def register_a_plugin(self, cls):
        if hasattr(cls, 'file_types'):
            PluginManager.register_a_plugin(self, cls)
            pypi_name = _get_me_pypi_package_name(cls.__module__)
            for file_type in cls.file_types:
                self._register_a_plugin(
                    cls.action, file_type, cls, pypi_name)
                manager.register_a_file_type(
                    file_type, cls.stream_type, None)
        else:
            self._logger.debug(
                "not register abstract interface %s" % cls.__name__)

    def _register_a_plugin(self, action, file_type, plugin, library):
        self.loaded_registry[file_type][library] = plugin

    def get_a_plugin(self, action, file_type, library):
        __file_type = file_type.lower()
        registry = self.loaded_registry

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
        plugins = self.known_plugins.get(file_type, None)
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

    def get_all_formats(self):
        all_formats = set(list(self.loaded_registry.keys()) +
                          list(self.known_plugins.keys()))
        all_formats = all_formats.difference(set([constants.DB_SQL,
                                                  constants.DB_DJANGO]))
        return all_formats


def _get_me_pypi_package_name(module_name):
    root_module_name = module_name.split('.')[0]
    return root_module_name.replace('_', '-')


readers = IOManager(READER_PLUGIN, ioutils.AVAILABLE_READERS)
writers = IOManager(WRITER_PLUGIN, ioutils.AVAILABLE_WRITERS)


def load_plugins(prefix, path, black_list, white_list):
    scan_plugins(
        prefix, constants.DEFAULT_PLUGIN_NAME,
        path, black_list, white_list)
