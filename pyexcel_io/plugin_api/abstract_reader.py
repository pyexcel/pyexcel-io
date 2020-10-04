from pyexcel_io._compact import OrderedDict


class IReader(object):
    def read_all(self):
        result = OrderedDict()
        for index, sheet in enumerate(self.content_array):
            result.update({sheet.name: self.read_sheet(index).to_array()})
        return result

    def sheet_names(self):
        return [content.name for content in self.content_array]

    def __len__(self):
        return len(self.content_array)
