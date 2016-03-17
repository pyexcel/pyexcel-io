from .book import ReaderFactory, WriterFactory
from .constants import MESSAGE_ERROR_02


def load_data_new(file_name=None,
                  file_content=None,
                  file_stream=None,
                  file_type=None,
                  sheet_name=None,
                  sheet_index=None,
                  **keywords):
    """Load data from any supported excel formats

    :param filename: actual file name, a file stream or actual content
    :param file_type: used only when filename is not a physial file name
    :param sheet_name: the name of the sheet to be loaded
    :param sheet_index: the index of the sheet to be loaded
    :param keywords: any other parameters
    """
    result = {}
    number_of_none_inputs = list(filter(lambda x: x is not None,
                                        [file_name, file_content, file_stream]))
    if len(number_of_none_inputs) != 1:
        raise IOError(MESSAGE_ERROR_02)
    if file_type is None:
        file_type = file_name.split(".")[-1]
    reader = ReaderFactory.create_reader(file_type)
    if file_name:
        reader.open(file_name, **keywords)
    elif file_content:
        reader.open_content(file_content, **keywords)
    elif file_stream:
        reader.open_stream(file_stream, **keywords)
    if sheet_name:
        result = reader.read_sheet_by_name(sheet_name)
    elif sheet_index:
        result = reader.read_sheet_by_index(sheet_index)
    else:
        result = reader.read_all()
    reader.close()
    return result


def get_writer_new(file_name=None, file_stream=None, file_type=None, **keywords):
    number_of_none_inputs = list(filter(lambda x: x is not None,
                                        [file_name, file_stream]))
    if len(number_of_none_inputs) != 1:
        raise IOError(MESSAGE_ERROR_02)
    file_type_given = True
    if file_type is None:
        file_type = file_name.split(".")[-1]
        file_type_given = False

    writer = WriterFactory.create_writer(file_type)
    if file_name:
        if file_type_given:
            writer.open_content(file_name, file_type=file_type, **keywords)
        else:
            writer.open(file_name, **keywords)
    elif file_stream:
        writer.open_stream(file_stream, **keywords)
    else:
        raise IOError("Wrong arguments")
    return writer
