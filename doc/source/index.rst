.. pyexcel_io documentation master file, created by
   sphinx-quickstart on Fri May 08 09:33:05 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

`pyexcel-io` - Let you focus on data, instead of file formats
================================================================================


:Author: C.W.
:Source code: http://github.com/pyexcel/pyexcel-io
:Issues: http://github.com/pyexcel/pyexcel-io/issues
:License: New BSD License
:Version: |version|
:Generated: |today|

Introduction
--------------------------------------------------------------------------------

**pyexcel-io** provides **one** application programming interface(API) to read
and write data in different excel formats. It makes information processing
involving excel files a simple task. The data in excel files can be turned into
an ordered dictionary with least code. This library focuses on data processing
using excel files as storage media hence fonts, colors and charts were not and
will not be considered.

It was created due to the lack of uniform programming interface to access data
in different excel formats. A developer needs to use different methods of
different libraries to read the same data in different excel formats, hence
the resulting code is cluttered and unmaintainable. This is a challenge posed
by users who do not know or care about the differences in excel file formats.
Instead of educating the users about the specific excel format a data processing
application supports, the library takes up the challenge and promises to support
all known excel formats.

All great work have done by individual library developers. This library unites
only the data access API. With that said, **pyexcel-io** also bring something
new on the table: :ref:`"csvz" and "tsvz"<csvz>` format, new format names
as of 2014. They are invented and supported by `pyexcel-io`_.

Getting the source
--------------------------------------------------------------------------------

Source code is hosted in github. You can get it using git client::

    $ git clone http://github.com/pyexcel/pyexcel-io.git

Installation
--------------------------------------------------------------------------------

You can install it via pip::

    $ pip install pyexcel-io

For individual excel file formats, please install them as you wish:

.. _a-map-of-plugins-and-file-formats:
.. table:: a map of plugins and supported excel file formats

   ============== ======================= ============= ==================   
   Package name   Supported file formats  Dependencies  Python versions     
   ============== ======================= ============= ==================   
   `pyexcel-io`_  csv, csvz [#f1]_, tsv,                2.6, 2.7, 3.3, 
                                                        3.4, pypy  
                  tsvz [#f2]_
   `xls`_         xls, xlsx(read only),   xlrd, xlwt    2.6, 2.7, 3.3,
                                                        3.4, pypy
                  xlsm(read only)
   `xlsx`_        xlsx                    openpyxl      2.6, 2.7, 3.3,
                                                        3.4, pypy   
   `ods3`_        ods                     ezodf, lxml   2.6, 2.7, 3.3, 3.4
   `ods`_         ods (python 2.6, 2.7)   odfpy         2.6, 2.7          
   ============== ======================= ============= ==================

After that, you can start get and save data in the loaded format. There
are two plugins for the same file format, e.g. pyexcel-ods3 and pyexcel-ods.
If you want to choose one, please try pip uninstall the un-wanted one. And if
you want to have both installed but wanted to use one of them for a function
call(or file type) and the other for another function call(or file type), you can
pass on "library" option to get_data and save_data.

.. table:: Plugin compatibility table

    ============= ======= ======== ======= ======== =========
    `pyexcel-io`_ `xls`_  `xlsx`_  `ods`_  `ods3`_  `text`_       
    ============= ======= ======== ======= ======== =========
    0.2.0         0.2.0   0.2.0    0.2.0   0.2.0    N/A
    0.1.0         0.1.0   0.1.0    0.1.0   0.1.0    0.1.0
    ============= ======= ======== ======= ======== =========

.. _pyexcel-io: https://github.com/pyexcel/pyexcel-io
.. _xls: https://github.com/pyexcel/pyexcel-xls
.. _xlsx: https://github.com/pyexcel/pyexcel-xlsx
.. _ods: https://github.com/pyexcel/pyexcel-ods
.. _ods3: https://github.com/pyexcel/pyexcel-ods3
.. _text: https://github.com/pyexcel/pyexcel-text

.. note::
   pyexcel-text is no longer a plugin of pyexcel-io but a direct plugin of pyexcel

Special note
--------------------------------------------------------------------------------
   migration_from_dot_1_to_dot_2


Tutorial
--------------------------------------------------------------------------------

.. toctree::
   :maxdepth: 2

   plaincsv
   extendedcsv
   csvz
   sqlalchemy
   django
   extensions


API
--------------------------------------------------

.. currentmodule:: pyexcel_io

.. autosummary::
   :toctree: api/
   
   get_data
   save_data


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


.. rubric:: Footnotes

.. [#f1] zipped csv file
.. [#f2] zipped tsv file
