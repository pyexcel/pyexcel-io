class ISheet(object):
    def to_array(self):
        data = []
        for row in self.row_iterator():
            my_row = []
            for element in self.column_iterator(row):
                my_row.append(element)
            data.append(my_row)
        return data


class ISheetWriter(object):
    def write_array(self, table):
        """
        For standalone usage, write an array
        """
        for row in table:
            self.write_row(row)
