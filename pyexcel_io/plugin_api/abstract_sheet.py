class ISheet(object):
    def row_iterator(self):
        raise NotImplementedError("")

    def column_iterator(self, column):
        raise NotImplementedError("")


class ISheetWriter(object):
    def write_array(self, table):
        """
        For standalone usage, write an array
        """
        for row in table:
            self.write_row(row)
