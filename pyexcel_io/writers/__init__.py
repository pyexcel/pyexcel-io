"""
    pyexcel_io.writers
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    file writers

    :copyright: (c) 2014-2017 by Onni Software Ltd.
    :license: New BSD License, see LICENSE for more details
"""
from pyexcel_io.plugins import IORegistry


__pyexcel_io_plugins__ = IORegistry(__name__).add_a_writer(
    submodule='csvw',
    file_types=['csv'],
    stream_type='text'
).add_a_writer(
    submodule='tsv',
    file_types=['tsv'],
    stream_type='text'
).add_a_writer(
    submodule='csvz',
    file_types=['csvz'],
    stream_type='binary'
).add_a_writer(
    submodule='tsvz',
    file_types=['tsvz'],
    stream_type='binary'
)
