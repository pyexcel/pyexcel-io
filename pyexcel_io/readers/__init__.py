"""
    pyexcel_io.readers
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    file readers

    :copyright: (c) 2014-2017 by Onni Software Ltd.
    :license: New BSD License, see LICENSE for more details
"""
from pyexcel_io.plugins import IORegistry


__pyexcel_io_plugins__ = IORegistry(__name__).add_a_reader(
    submodule='csvr',
    file_types=['csv'],
    stream_type='text'
).add_a_reader(
    submodule='tsv',
    file_types=['tsv'],
    stream_type='text'
).add_a_reader(
    submodule='csvz',
    file_types=['csvz'],
    stream_type='binary'
).add_a_reader(
    submodule='tsvz',
    file_types=['csvz'],
    stream_type='binary'
)
