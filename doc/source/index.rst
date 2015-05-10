.. pyexcel_io documentation master file, created by
   sphinx-quickstart on Fri May 08 09:33:05 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

`pyexcel-io` - Let you focus on data, instead of file formats
================================================================================


:Author: C.W.
:Source code: http://github.com/chfw/pyexcel-io
:Issues: http://github.com/chfw/pyexcel-io/issues
:License: New BSD License
:Version: |version| unreleased yet
:Generated: |today|

Introduction
--------------------------------------------------------------------------------

**pyexcel-io** is a wrapper library that provides **one** application
programming interface to read and write data in different excel formats.
This library makes information processing involving excel files a
simple task. The data in excel files can be turned into an ordered dictionary
with least code, vice versa. This library focuses on data processing using
excel files as storage media hence fonts, colors and charts were not and
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
only the data access code. With that said, pyexcel also bring something new on
the table: :ref:`"csvz" and "tsvz"<csvz>` format, new format names as of 2014.
They are invented and supported by `pyexcel-io`_.

Getting the source
--------------------------------------------------------------------------------

Source code is hosted in github. You can get it using git client::

    $ git clone http://github.com/chfw/pyexcel-io.git

Installation
--------------------------------------------------------------------------------

You can install it via pip::

    $ pip install pyexcel-io

For individual excel file formats, please install them as you wish:

.. _a-map-of-plugins-and-file-formats:
.. table:: a map of plugins and supported excel file formats

   ================ ============================================================ ============= ======================== =============================   
   Plugin           Supported file formats                                       Dependencies  Python versions           Comments                       
   ================ ============================================================ ============= ======================== =============================   
   `pyexcel-io`_         csv, csvz [#f1]_, tsv, tsvz [#f2]_                                    2.6, 2.7, 3.3, 3.4, pypy                                
   `xls`_           xls, xlsx(read only), xlsm(read only)                        xlrd, xlwt    2.6, 2.7, 3.3, 3.4, pypy supports reading xlsx as well
   `xlsx`_          xlsx                                                         openpyxl      2.6, 2.7, 3.3, 3.4, pypy                                 
   `ods3`_          ods                                                          ezodf, lxml   2.6, 2.7, 3.3, 3.4                                               
   `ods`_           ods (python 2.6, 2.7)                                        odfpy         2.6, 2.7                                             
   ================ ============================================================ ============= ======================== =============================

Please import them before you start to access the desired file formats::

    import pyexcel_plugin

.. table:: Plugin compatibility table

    ============= =========== ============ ============ ============
    `pyexcel-io`_ `xls`_      `xlsx`_      `ods`_       `ods3`_        
    ============= =========== ============ ============ ============
    0.0.4         0.0.7       0.0.6        0.0.6        0.0.8       
    0.0.3         0.0.6       0.0.5        0.0.5        0.0.7       
    0.0.2         0.0.3-0.0.5 0.0.2-0.0.4  0.0.4        0.0.5-0.0.6 
    0.0.2         0.0.3-0.0.5 0.0.2-0.0.4  0.0.4        0.0.5-0.0.6 
    0.0.2         0.0.3-0.0.5 0.0.2-0.0.4  0.0.4        0.0.5-0.0.6 
    0.0.2         0.0.3-0.0.5 0.0.2-0.0.4  0.0.4        0.0.5-0.0.6 
    0.0.1         0.0.2       0.0.1        0.0.3        0.0.4       
    ============= =========== ============ ============ ============

.. _pyexcel-io: https://github.com/chfw/pyexcel-io
.. _xls: https://github.com/chfw/pyexcel-xls
.. _xlsx: https://github.com/chfw/pyexcel-xlsx
.. _ods: https://github.com/chfw/pyexcel-ods
.. _ods3: https://github.com/chfw/pyexcel-ods3


Contents:

.. toctree::
   :maxdepth: 2

   plaincsv
   csvz
   sqlalchemy
   django

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


.. rubric:: Footnotes

.. [#f1] zipped csv file
.. [#f2] zipped tsv file
