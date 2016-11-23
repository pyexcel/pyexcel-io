Change log
================================================================================

unreleased
--------------------------------------------------------------------------------

Updated
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

#. `#19 <https://github.com/pyexcel/pyexcel-io/issues/19>`__, use cString by default

0.24 - unreleased
--------------------------------------------------------------------------------

Updated
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

#. `#23 <https://github.com/pyexcel/pyexcel-io/issues/23>`__, Failed to convert
   long integer string in python 2 to its actual value

0.23 - 16.09.2016
--------------------------------------------------------------------------------

Added
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

#. `#21 <https://github.com/pyexcel/pyexcel-io/issues/21>`__, choose subset from data base tables for export
#. `#22 <https://github.com/pyexcel/pyexcel-io/issues/22>`__, custom renderer if given `row_renderer` as parameter.

0.22 - 31.08.2016
--------------------------------------------------------------------------------

Added
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

#. support pagination. two pairs: start_row, row_limit and start_column, column_limit
   help you deal with large files.
#. `skip_empty_rows=True` was introduced. To include empty rows, put it to False.

Updated
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

#. `#20 <https://github.com/pyexcel/pyexcel-io/issues/20>`__, pyexcel-io attempts
   to parse cell contents of 'infinity' as a float/int, crashes


0.2.1 - 11.07.2016
--------------------------------------------------------------------------------


Added
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

#. csv format: handle utf-16 encoded csv files. Potentially being able to decode other formats if correct "encoding" is provided
#. csv format: write utf-16 encoded files. Potentially other encoding is also supported
#. support stdin as input stream and stdout as output stream

Updated
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

#. Attention, user of pyexcel-io! No longer io stream validation is performed in python 3. The guideline is: io.StringIO for csv, tsv only, otherwise BytesIO for xlsx, xls, ods. You can use RWManager.get_io to produce a correct stream type for you.
#. `#15 <https://github.com/pyexcel/pyexcel-io/issues/15>`__, support foreign django/sql foreign key
   
0.2.0 - 01.06.2016
--------------------------------------------------------------------------------

Added
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

#. autoload of pyexcel-io plugins
#. auto detect `datetime`, `float` and `int`. Detection can be switched off by
   `auto_detect_datetime`, `auto_detect_float`, `auto_detect_int`

   
0.1.0 - 17.01.2016
--------------------------------------------------------------------------------

Added
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# yield key word to return generator as content
