"""
    pyexcel_io.database
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    database data importer and exporter

    :copyright: (c) 2014-2020 by Onni Software Ltd.
    :license: New BSD License, see LICENSE for more details
"""
from pyexcel_io.plugins import IOPluginInfoChain, NewIOPluginInfoChain
from pyexcel_io.constants import DB_SQL, DB_DJANGO

IOPluginInfoChain(__name__).add_a_writer(
    relative_plugin_class_path="importers.django.DjangoBookWriter",
    file_types=[DB_DJANGO],
).add_a_writer(
    relative_plugin_class_path="importers.sqlalchemy.SQLBookWriter",
    file_types=[DB_SQL],
)

NewIOPluginInfoChain(__name__).add_a_reader(
    relative_plugin_class_path="exporters.django.DjangoBookReader",
    location="file",
    file_types=[DB_DJANGO],
).add_a_reader(
    relative_plugin_class_path="exporters.django.DjangoBookReader",
    location="memory",
    file_types=[DB_DJANGO],
).add_a_reader(
    relative_plugin_class_path="exporters.django.DjangoBookReader",
    location="content",
    file_types=[DB_DJANGO],
).add_a_reader(
    relative_plugin_class_path="exporters.sqlalchemy.SQLBookReader",
    location="file",
    file_types=[DB_SQL],
).add_a_reader(
    relative_plugin_class_path="exporters.sqlalchemy.SQLBookReader",
    location="memory",
    file_types=[DB_SQL],
).add_a_reader(
    relative_plugin_class_path="exporters.sqlalchemy.SQLBookReader",
    location="content",
    file_types=[DB_SQL],
)
