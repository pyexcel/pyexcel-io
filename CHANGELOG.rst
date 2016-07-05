Change log
================================================================================

0.2.1 - unreleased
--------------------------------------------------------------------------------

Updated
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

#. Attention, user of pyexcel-io! No longer io stream validation is performed in python 3. The guideline is: io.StringIO for csv, tsv only, otherwise BytesIO for xlsx, xls, ods. You can use RWManager.get_io to produce a correct stream type for you.
#. csv format: handle utf-16 encoded csv files. Potentially being able to decode other formats if correct "encoding" is provided

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
