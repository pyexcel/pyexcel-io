class TableExportAdapter(object):
    def __init__(self, model, export_columns=None):
        self.model = model
        self.export_columns = export_columns

    @property
    def name(self):
        return self.get_name()

    def get_name(self):
        return self.model._meta.model_name


class TableExporter(object):
    def __init__(self):
        self.adapters = []

    def append(self, import_adapter):
        self.adapters.append(import_adapter)


class TableImporter(object):
    def __init__(self):
        self.__adapters = {}

    def append(self, import_adapter):
        self.__adapters[import_adapter.get_name()] = import_adapter

    def get(self, name):
        return self.__adapters.get(name, None)


class TableImportAdapter(TableExportAdapter):

    class InOutParameter(object):
        def __init__(self):
            self.output = None
            self.input = None

    def __init__(self, model):
        TableExportAdapter.__init__(self, model)
        self.__column_names = self.InOutParameter()
        self.__column_name_mapping_dict = self.InOutParameter()
        self.__row_initializer = self.InOutParameter()
        self._process_parameters()

    @property
    def row_initializer(self):
        return self.__row_initializer.output

    @property
    def column_names(self):
        return self.__column_names.output

    @property
    def column_name_mapping_dict(self):
        return self.__column_name_mapping_dict.output

    @row_initializer.setter
    def row_initializer(self, a_function):
        self.__row_initializer.input = a_function
        self._process_parameters()

    @column_names.setter
    def column_names(self, column_names):
        self.__column_names.input = column_names
        self._process_parameters()

    @column_name_mapping_dict.setter
    def column_name_mapping_dict(self, mapping_dict):
        self.__column_name_mapping_dict.input = mapping_dict
        self._process_parameters()

    def _process_parameters(self):

        if self.__row_initializer.input is None:
            self.__row_initializer.output = None
        else:
            self.__row_initializer.output = self.__row_initializer.input
        if isinstance(self.__column_name_mapping_dict.input, list):
            self.__column_names.output = self.__column_name_mapping_dict.input
            self.__column_name_mapping_dict.output = None
        elif isinstance(self.__column_name_mapping_dict.input, dict):
            if self.__column_names.input:
                self.__column_names.output = [
                    self.__column_name_mapping_dict.input[name]
                    for name in self.__column_names.input]
                self.__column_name_mapping_dict.output = None
        if self.__column_names.output is None:
            self.__column_names.output = self.__column_names.input
