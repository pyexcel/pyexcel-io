from pyexcel_io.constants import DB_DJANGO, DB_SQL


__pyexcel_io_plugins__ = [
    {
        'plugin_type': 'pyexcel-io reader',
        'submodule': 'importers.django',
        'file_types': [DB_DJANGO],
        'stream_type': None
    },
    {
        'plugin_type': 'pyexcel-io reader',
        'submodule': 'importers.sqlalchemy',
        'file_types': [DB_SQL],
        'stream_type': None
    },
    {
        'plugin_type': 'pyexcel-io writer',
        'submodule': 'exporters.django',
        'file_types': [DB_DJANGO],
        'stream_type': None
    },
    {
        'plugin_type': 'pyexcel-io writer',
        'submodule': 'exporters.sqlalchemy',
        'file_types': [DB_SQL],
        'stream_type': None
    }
]
