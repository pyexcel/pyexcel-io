Change log
================================================================================

0.5.17 - 04.04.2019
--------------------------------------------------------------------------------

updated
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

#. `#68 <https://github.com/pyexcel/pyexcel-io/issues/68>`_: Raise IOError when
   the data file does not exist

0.5.16 - 19.03.2019
--------------------------------------------------------------------------------

updated
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

#. `#67 <https://github.com/pyexcel/pyexcel-io/issues/67>`_: fix conversion
   issue for long type on python 2.7 for ods

0.5.15 - 16.03.2019
--------------------------------------------------------------------------------

updated
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

#. `pyexcel-ods#33 <https://github.com/pyexcel/pyexcel-ods/issues/33>`_: fix
   integer comparision error on i586

0.5.14 - 21.02.2019
--------------------------------------------------------------------------------

updated
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

#. `#65 <https://github.com/pyexcel/pyexcel-io/issues/65>`_: add
   tests/__init__.py because python2.7 setup.py test needs it

0.5.13 - 12.02.2019
--------------------------------------------------------------------------------

updated
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

#. `#63 <https://github.com/pyexcel/pyexcel-io/issues/63>`_: Version 0.5.12
   prevents xslx and ods plugin from being loaded

0.5.12 - 9.02.2019
--------------------------------------------------------------------------------

updated
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

#. `#60 <https://github.com/pyexcel/pyexcel-io/issues/60>`_: include tests in
   tar ball
#. `#61 <https://github.com/pyexcel/pyexcel-io/issues/61>`_: enable python
   setup.py test

0.5.11 - 3.12.2018
--------------------------------------------------------------------------------

updated
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

#. `#59 <https://github.com/pyexcel/pyexcel-io/issues/59>`_: Please use
   scan_plugins_regex, which lml 0.7 complains about

0.5.10 - 27.11.2018
--------------------------------------------------------------------------------

added
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

#. `#57 <https://github.com/pyexcel/pyexcel-io/issues/57>`_, long type will not
   be written in ods. please use string type. And if the integer is equal or
   greater than 10 to the power of 16, it will not be written either in ods. In
   both situation, IntegerPrecisionLossError will be raised. And this version
   enables pyexcel-ods and pyexcel-ods3 to do so.

0.5.9.1 - 30.08.2018
--------------------------------------------------------------------------------

updated
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

#. `#53 <https://github.com/pyexcel/pyexcel-io/issues/53>`_, upgrade lml
   dependency to at least 0.0.2

0.5.9 - 23.08.2018
--------------------------------------------------------------------------------

added
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

#. `pyexcel#148 <https://github.com/pyexcel/pyexcel/issues/148>`_, support
   force_file_type

0.5.8 - 16.08.2018
--------------------------------------------------------------------------------

added
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

#. `#49 <https://github.com/pyexcel/pyexcel-io/issues/49>`_, support additional
   options when detecting float values in csv format. default_float_nan,
   ignore_nan_text

0.5.7 - 02.05.2018
--------------------------------------------------------------------------------

fixed
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

#. `#48 <https://github.com/pyexcel/pyexcel-io/issues/48>`_, turn off pep 0515
#. `#47 <https://github.com/pyexcel/pyexcel-io/issues/47>`_, csv reader cannot
   handle relative file names

0.5.6 - 11.01.2018
--------------------------------------------------------------------------------

fixed
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

#. `#46 <https://github.com/pyexcel/pyexcel-io/issues/46>`_, expose `bulk_save`
   to developer

0.5.5 - 23.12.2017
--------------------------------------------------------------------------------

fixed
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

#. Issue `#45 <https://github.com/pyexcel/pyexcel-io/issues/45>`_, csv reader
   throws exception because google app engine does not support mmap. People who
   are not working with google app engine, need not to take this update. Enjoy
   your Christmas break.

0.5.4 - 10.11.2017
--------------------------------------------------------------------------------

updated
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

#. PR `#44 <https://github.com/pyexcel/pyexcel-io/pull/44>`_, use unicodewriter
   for csvz writers.

0.5.3 - 23.10.2017
--------------------------------------------------------------------------------

updated
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

#. pyexcel `pyexcel#105 <https://github.com/pyexcel/pyexcel/issues/105>`_,
   remove gease from setup_requires, introduced by 0.5.2.
#. remove python2.6 test support

0.5.2 - 20.10.2017
--------------------------------------------------------------------------------

added
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

#. `pyexcel#103 <https://github.com/pyexcel/pyexcel/issues/103>`_, include
   LICENSE file in MANIFEST.in, meaning LICENSE file will appear in the released
   tar ball.

0.5.1 - 02.09.2017
--------------------------------------------------------------------------------

Fixed
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

#. `pyexcel-ods#25 <https://github.com/pyexcel/pyexcel-ods/issues/25>`_,
   Unwanted dependency on pyexcel.

0.5.0 - 30.08.2017
--------------------------------------------------------------------------------

Added
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

#. Collect all data type conversion codes as service.py.

Updated
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

#. `#19 <https://github.com/pyexcel/pyexcel-io/issues/19>`_, use cString by
   default. For python, it will be a performance boost

0.4.4 - 08.08.2017
--------------------------------------------------------------------------------

Updated
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

#. `#42 <https://github.com/pyexcel/pyexcel-io/issues/42>`_, raise exception if
   database table name does not match the sheet name

0.4.3 - 29.07.2017
--------------------------------------------------------------------------------

Updated
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

#. `#41 <https://github.com/pyexcel/pyexcel-io/issues/41>`_, walk away
   gracefully when mmap is not available.

0.4.2 - 05.07.2017
--------------------------------------------------------------------------------

Updated
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

#. `#37 <https://github.com/pyexcel/pyexcel-io/issues/37>`_, permanently fix the
   residue folder pyexcel by release all future releases in a clean clone.

0.4.1 - 29.06.2017
--------------------------------------------------------------------------------

Updated
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

#. `#39 <https://github.com/pyexcel/pyexcel-io/issues/39>`_, raise exception
   when bulk save in django fails. Please `bulk_save=False` if you as the
   developer choose to save the records one by one if bulk_save cannot be used.
   However, exception in one-by-one save case will be raised as well. This
   change is made to raise exception in the first place so that you as the
   developer will be suprised when it was deployed in production.

0.4.0 - 19.06.2017
--------------------------------------------------------------------------------

Updated
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

#. 'built-in' as the value to the parameter 'library' as parameter to invoke
   pyexcel-io's built-in csv, tsv, csvz, tsvz, django and sql won't work. It is
   renamed to 'pyexcel-io'.
#. built-in csv, tsv, csvz, tsvz, django and sql are lazy loaded.
#. pyexcel-io plugin interface has been updated. v0.3.x plugins won't work.
#. `#32 <https://github.com/pyexcel/pyexcel-io/issues/32>`_, csv and csvz file
   handle are made sure to be closed. File close mechanism is enfored.
#. iget_data function is introduced to cope with dangling file handle issue.

Removed
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

#. Removed plugin loading code and lml is used instead

0.3.4 - 18.05.2017
--------------------------------------------------------------------------------

Updated
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

#. `#33 <https://github.com/pyexcel/pyexcel-io/issues/33>`_, handle mmap object
   differently given as file content. This issue has put in a priority to single
   sheet csv over multiple sheets in a single memory stream. The latter format
   is pyexcel own creation but is rarely used. In latter case,
   multiple_sheet=True should be passed along get_data.
#. `#34 <https://github.com/pyexcel/pyexcel-io/issues/34>`_, treat mmap object
   as a file content.
#. `#35 <https://github.com/pyexcel/pyexcel-io/issues/35>`_, encoding parameter
   take no effect when given along with file content
#. use ZIP_DEFALTED to really do the compression

0.3.3 - 30.03.2017
--------------------------------------------------------------------------------

Updated
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

#. `#31 <https://github.com/pyexcel/pyexcel-io/issues/31>`_, support pyinstaller

0.3.2 - 26.01.2017
--------------------------------------------------------------------------------

Updated
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

#. `#29 <https://github.com/pyexcel/pyexcel-io/issues/29>`_, change
   skip_empty_rows to False by default

0.3.1 - 21.01.2017
--------------------------------------------------------------------------------

Added
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

#. updated versions of extra packages

Updated
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

#. `#23 <https://github.com/pyexcel/pyexcel-io/issues/23>`_, provide helpful
   message when old pyexcel plugin exists
#. restored previously available diagnosis message for missing libraries

0.3.0 - 22.12.2016
--------------------------------------------------------------------------------

Added
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

#. lazy loading of plugins. for example, pyexcel-xls is not entirely loaded
   until xls format is used at its first attempted reading or writing. Since it
   is loaded, it will not be loaded in the second io action.
#. `pyexcel-xls#11 <https://github.com/pyexcel/pyexcel-xls/issues/11>`_, make
   case-insensitive for file type

0.2.6 - 21.12.2016
--------------------------------------------------------------------------------

Updated
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

#. `#24 <https://github.com/pyexcel/pyexcel-io/issues/24>`__, pass on batch_size

0.2.5 - 20.12.2016
--------------------------------------------------------------------------------

Updated
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

#. `#26 <https://github.com/pyexcel/pyexcel-io/issues/26>`__, performance issue
   with getting the number of columns.

0.2.4 - 24.11.2016
--------------------------------------------------------------------------------

Updated
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

#. `#23 <https://github.com/pyexcel/pyexcel-io/issues/23>`__, Failed to convert
   long integer string in python 2 to its actual value

0.2.3 - 16.09.2016
--------------------------------------------------------------------------------

Added
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

#. `#21 <https://github.com/pyexcel/pyexcel-io/issues/21>`__, choose subset from
   data base tables for export
#. `#22 <https://github.com/pyexcel/pyexcel-io/issues/22>`__, custom renderer if
   given `row_renderer` as parameter.

0.2.2 - 31.08.2016
--------------------------------------------------------------------------------

Added
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

#. support pagination. two pairs: start_row, row_limit and start_column,
   column_limit help you deal with large files.
#. `skip_empty_rows=True` was introduced. To include empty rows, put it to
   False.

Updated
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

#. `#20 <https://github.com/pyexcel/pyexcel-io/issues/20>`__, pyexcel-io
   attempts to parse cell contents of 'infinity' as a float/int, crashes

0.2.1 - 11.07.2016
--------------------------------------------------------------------------------

Added
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

#. csv format: handle utf-16 encoded csv files. Potentially being able to decode
   other formats if correct "encoding" is provided
#. csv format: write utf-16 encoded files. Potentially other encoding is also
   supported
#. support stdin as input stream and stdout as output stream

Updated
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

#. Attention, user of pyexcel-io! No longer io stream validation is performed in
   python 3. The guideline is: io.StringIO for csv, tsv only, otherwise BytesIO
   for xlsx, xls, ods. You can use RWManager.get_io to produce a correct stream
   type for you.
#. `#15 <https://github.com/pyexcel/pyexcel-io/issues/15>`__, support foreign
   django/sql foreign key

0.2.0 - 01.06.2016
--------------------------------------------------------------------------------

Added
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

#. autoload of pyexcel-io plugins
#. auto detect `datetime`, `float` and `int`. Detection can be switched off by
   `auto_detect_datetime`, `auto_detect_float`, `auto_detect_int`

0.1.0 - 17.01.2016
--------------------------------------------------------------------------------

Added
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

#. yield key word to return generator as content
