from pyexcel_io.constants import DB_DJANGO, DB_SQL


__pyexcel_io_plugins__ = [
    {
        'plugin_type': 'pyexcel io plugin',
        'submodule': 'django',
        'file_types': [DB_DJANGO],
        'stream_type': None
    },
    {
        'plugin_type': 'pyexcel io plugin',
        'submodule': 'sql',
        'file_types': [DB_SQL],
        'stream_type': 'string'
    }
]
