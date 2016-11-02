

def load_data(filename,
              file_type=None,
              sheet_name=None,
              sheet_index=None,
              **keywords):
    raise NotImplementedError(
        "Removed since 0.3.0! Please use get_data instead.")


def get_writer(filename, file_type=None, **keywords):
    raise NotImplementedError(
        "Removed since 0.3.0! Please use save_data instead.")
