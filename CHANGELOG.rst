Change log
================================================================================


deferred - unreleased
--------------------------------------------------------------------------------

Updated
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

#. `#19 <https://github.com/pyexcel/pyexcel-io/issues/19>`_,
   use cString by default

0.3.3 - unreleased
--------------------------------------------------------------------------------

Updated
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

#. `#31 <https://github.com/pyexcel/pyexcel-io/issues/31>`_, support pyinstaller


0.3.2 - 26.01.2017
--------------------------------------------------------------------------------

Updated
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

#. `#29 <https://github.com/pyexcel/pyexcel-io/issues/29>`_, change
   skip_empty_rows to False by default

0.3.1 - 21.01.2017
--------------------------------------------------------------------------------

Added
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

#. updated versions of extra packages

Updated
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

#. `#23 <https://github.com/pyexcel/pyexcel-io/issues/23>`_, provide helpful
   message when old pyexcel plugin exists
#. restored previously available diagnosis message for missing libraries
   

0.3.0 - 22.12.2016
--------------------------------------------------------------------------------

Added
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

#. lazy loading of plugins. for example, pyexcel-xls is not entirely loaded
   until xls format is used at its first attempted reading or writing. Since
   it is loaded, it will not be loaded in the second io action.
#. `pyexcel-xls issue 11 <https://github.com/pyexcel/pyexcel-xls/issues/11>`_,
   make case-insensitive for file type


0.2.6 - 21.12.2016
--------------------------------------------------------------------------------

Updated
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

#. `#24 <https://github.com/pyexcel/pyexcel-io/issues/24>`__, pass on batch_size


0.2.5 - 20.12.2016
--------------------------------------------------------------------------------

Updated
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

#. `#26 <https://github.com/pyexcel/pyexcel-io/issues/26>`__, performance issue
   with getting the number of columns.

0.2.4 - 24.11.2016
--------------------------------------------------------------------------------

Updated
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

#. `#23 <https://github.com/pyexcel/pyexcel-io/issues/23>`__, Failed to convert
   long integer string in python 2 to its actual value

0.2.3 - 16.09.2016
--------------------------------------------------------------------------------

Added
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

#. `#21 <https://github.com/pyexcel/pyexcel-io/issues/21>`__, choose subset from
   data base tables for export
#. `#22 <https://github.com/pyexcel/pyexcel-io/issues/22>`__, custom renderer if
   given `row_renderer` as parameter.

0.2.2 - 31.08.2016
--------------------------------------------------------------------------------

Added
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

#. support pagination. two pairs: start_row, row_limit and start_column,
   column_limit help you deal with large files.
#. `skip_empty_rows=True` was introduced. To include empty rows, put it to False.

Updated
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

#. `#20 <https://github.com/pyexcel/pyexcel-io/issues/20>`__, pyexcel-io attempts
   to parse cell contents of 'infinity' as a float/int, crashes


0.2.1 - 11.07.2016
--------------------------------------------------------------------------------


Added
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

#. csv format: handle utf-16 encoded csv files. Potentially being able to decode
   other formats if correct "encoding" is provided
#. csv format: write utf-16 encoded files. Potentially other encoding is also
   supported
#. support stdin as input stream and stdout as output stream

Updated
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

#. Attention, user of pyexcel-io! No longer io stream validation is performed
   in python 3. The guideline is: io.StringIO for csv, tsv only, otherwise
   BytesIO for xlsx, xls, ods. You can use RWManager.get_io to produce a correct
   stream type for you.
#. `#15 <https://github.com/pyexcel/pyexcel-io/issues/15>`__, support foreign
   django/sql foreign key
   
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
