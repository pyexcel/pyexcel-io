"""
    pyexcel_io.readers
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    file readers

    :copyright: (c) 2014-2017 by Onni Software Ltd.
    :license: New BSD License, see LICENSE for more details
"""
from pyexcel_io.plugins import IORegistry


IORegistry(__name__).add_a_reader(
    submodule='csvr.CSVBookReader',
    file_types=['csv'],
    stream_type='text'
).add_a_reader(
    submodule='tsv.TSVBookReader',
    file_types=['tsv'],
    stream_type='text'
).add_a_reader(
    submodule='csvz.CSVZipBookReader',
    file_types=['csvz'],
    stream_type='binary'
).add_a_reader(
    submodule='tsvz.TSVZipBookReader',
    file_types=['tsvz'],
    stream_type='binary'
)
