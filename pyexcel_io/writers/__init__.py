"""
    pyexcel_io.writers
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    file writers

    :copyright: (c) 2014-2020 by Onni Software Ltd.
    :license: New BSD License, see LICENSE for more details
"""
from pyexcel_io.plugins import IOPluginInfoChain, NewIOPluginInfoChain

NewIOPluginInfoChain(__name__).add_a_writer(
    relative_plugin_class_path="csv_file_writer.CsvFileWriter",
    locations=["file", "content"],
    file_types=["csv"],
    stream_type="text",
).add_a_writer(
    relative_plugin_class_path="csv_memory_writer.CsvMemoryWriter",
    locations=["memory"],
    file_types=["csv"],
    stream_type="text",
).add_a_writer(
    relative_plugin_class_path="tsv_file_writer.TsvFileWriter",
    locations=["file", "content"],
    file_types=["tsv"],
    stream_type="text",
).add_a_writer(
    relative_plugin_class_path="tsv_memory_writer.TsvMemoryWriter",
    locations=["memory"],
    file_types=["tsv"],
    stream_type="text",
)

IOPluginInfoChain(__name__).add_a_writer(
    relative_plugin_class_path="csvz.CSVZipBookWriter",
    file_types=["csvz"],
    stream_type="binary",
).add_a_writer(
    relative_plugin_class_path="tsvz.TSVZipBookWriter",
    file_types=["tsvz"],
    stream_type="binary",
)
