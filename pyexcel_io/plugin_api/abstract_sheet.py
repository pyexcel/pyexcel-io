class Sheet(object):
    def to_array(self):
        data = []
        for row in self.row_iterator():
            my_row = []
            for element in self.column_iterator(row):
                my_row.append(element)
            data.append(my_row)
        return data
