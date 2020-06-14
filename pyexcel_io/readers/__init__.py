"""
    pyexcel_io.readers
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    file readers

    :copyright: (c) 2014-2020 by Onni Software Ltd.
    :license: New BSD License, see LICENSE for more details
"""
from pyexcel_io.plugins import IOPluginInfoChain, NewIOPluginInfoChain

IOPluginInfoChain(__name__).add_a_reader(
    relative_plugin_class_path="tsv.TSVBookReader",
    file_types=["tsv"],
    stream_type="text",
).add_a_reader(
    relative_plugin_class_path="csvz.CSVZipBookReader",
    file_types=["csvz"],
    stream_type="binary",
).add_a_reader(
    relative_plugin_class_path="tsvz.TSVZipBookReader",
    file_types=["tsvz"],
    stream_type="binary",
)

NewIOPluginInfoChain(__name__).add_a_reader(
    relative_plugin_class_path="csv_file_reader.FileReader",
    location="file",
    file_types=["csv"],
    stream_type="text",
).add_a_reader(
    relative_plugin_class_path="csv_content_reader.ContentReader",
    location="content",
    file_types=["csv"],
    stream_type="text",
).add_a_reader(
    relative_plugin_class_path="csv_memory_reader.MemoryReader",
    location="memory",
    file_types=["csv"],
    stream_type="text",
).add_a_reader(
    relative_plugin_class_path="tsv.TSVMemoryReader",
    location="memory",
    file_types=["tsv"],
    stream_type="text",
).add_a_reader(
    relative_plugin_class_path="tsv.TSVFileReader",
    location="file",
    file_types=["tsv"],
    stream_type="text",
).add_a_reader(
    relative_plugin_class_path="tsv.TSVContentReader",
    location="content",
    file_types=["tsv"],
    stream_type="text",
)
