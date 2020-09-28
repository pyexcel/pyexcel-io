from pyexcel_io._compact import OrderedDict


class IReader(object):
    def read_all(self):
        result = OrderedDict()
        for index, sheet in enumerate(self.content_array):
            result.update({sheet.name: self.read_sheet(index).to_array()})
        return result
