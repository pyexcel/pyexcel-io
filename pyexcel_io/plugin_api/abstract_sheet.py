class ISheet(object):
    def row_iterator(self):
        raise NotImplementedError("")

    def column_iterator(self, row):
        raise NotImplementedError("")


class ISheetWriter(object):
    def write_row(self, data_row):
        raise NotImplementedError("How does your sheet write a row of data")

    def write_array(self, table):
        """
        For standalone usage, write an array
        """
        for row in table:
            self.write_row(row)
