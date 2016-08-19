Change log
================================================================================

0.22 - unreleased
--------------------------------------------------------------------------------

Added
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

#. support pagination. two pairs: start_row, row_limit and start_column, column_limit
   help you deal with large files.

Updated
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

#. `#19 <https://github.com/pyexcel/pyexcel-io/issues/19>`__, use cString by default

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
