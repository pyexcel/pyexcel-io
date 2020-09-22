"""
    pyexcel_io.readers
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    file readers

    :copyright: (c) 2014-2020 by Onni Software Ltd.
    :license: New BSD License, see LICENSE for more details
"""
from pyexcel_io.plugins import NewIOPluginInfoChain

NewIOPluginInfoChain(__name__).add_a_reader(
    relative_plugin_class_path="csv_in_file.FileReader",
    location="file",
    file_types=["csv"],
    stream_type="text",
).add_a_reader(
    relative_plugin_class_path="csv_content.ContentReader",
    location="content",
    file_types=["csv"],
    stream_type="text",
).add_a_reader(
    relative_plugin_class_path="csv_in_memory.MemoryReader",
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
).add_a_reader(
    relative_plugin_class_path="csvz.FileReader",
    file_types=["csvz"],
    location="file",
    stream_type="binary",
).add_a_reader(
    relative_plugin_class_path="csvz.FileReader",
    file_types=["csvz"],
    location="memory",
    stream_type="binary",
).add_a_reader(
    relative_plugin_class_path="tsvz.TSVZipFileReader",
    file_types=["tsvz"],
    location="file",
    stream_type="binary",
).add_a_reader(
    relative_plugin_class_path="tsvz.TSVZipFileReader",
    file_types=["tsvz"],
    location="memory",
    stream_type="binary",
)
