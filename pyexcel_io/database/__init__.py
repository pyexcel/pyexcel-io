"""
    pyexcel_io.database
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    database data importer and exporter

    :copyright: (c) 2014-2017 by Onni Software Ltd.
    :license: New BSD License, see LICENSE for more details
"""
from pyexcel_io.plugins import IORegistry
from pyexcel_io.constants import DB_DJANGO, DB_SQL


__pyexcel_io_plugins__ = IORegistry(__name__).add_a_reader(
    submodule='importers.django',
    file_types=[DB_DJANGO]
).add_a_reader(
    submodule='importers.sqlalchemy',
    file_types=[DB_SQL],
).add_a_writer(
    submodule='exporters.django',
    file_types=[DB_DJANGO],
).add_a_writer(
    submodule='exporters.sqlalchemy',
    file_types=[DB_SQL]
)
