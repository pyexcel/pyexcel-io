"""
    pyexcel_io.database
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    database data importer and exporter

    :copyright: (c) 2014-2017 by Onni Software Ltd.
    :license: New BSD License, see LICENSE for more details
"""
from pyexcel_io.plugins import IORegistry
from pyexcel_io.constants import DB_DJANGO, DB_SQL


IORegistry(__name__).add_a_reader(
    submodule='exporters.django.DjangoBookReader',
    file_types=[DB_DJANGO]
).add_a_reader(
    submodule='exporters.sqlalchemy.SQLBookReader',
    file_types=[DB_SQL],
).add_a_writer(
    submodule='importers.django.DjangoBookWriter',
    file_types=[DB_DJANGO],
).add_a_writer(
    submodule='importers.sqlalchemy.SQLBookWriter',
    file_types=[DB_SQL]
)
