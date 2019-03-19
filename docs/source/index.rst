.. pyexcel_io documentation master file, created by
   sphinx-quickstart on Fri May 08 09:33:05 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

`pyexcel-io` - Let you focus on data, instead of file formats
================================================================================

:Author: C.W.
:Source code: http://github.com/pyexcel/pyexcel-io.git
:Issues: http://github.com/pyexcel/pyexcel-io/issues
:License: New BSD License
:Released: |version|
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


Installation
--------------------------------------------------------------------------------


You can install pyexcel-io via pip:

.. code-block:: bash

    $ pip install pyexcel-io


or clone it and install it:

.. code-block:: bash

    $ git clone https://github.com/pyexcel/pyexcel-io.git
    $ cd pyexcel-io
    $ python setup.py install

For individual excel file formats, please install them as you wish:

.. _file-format-list:
.. _a-map-of-plugins-and-file-formats:

.. table:: A list of file formats supported by external plugins

   ======================== ======================= ================= ==================
   Package name              Supported file formats  Dependencies     Python versions
   ======================== ======================= ================= ==================
   `pyexcel-io`_            csv, csvz [#f1]_, tsv,                    2.6, 2.7, 3.3,
                            tsvz [#f2]_                               3.4, 3.5, 3.6
                                                                      pypy
   `pyexcel-xls`_           xls, xlsx(read only),   `xlrd`_,          same as above
                            xlsm(read only)         `xlwt`_
   `pyexcel-xlsx`_          xlsx                    `openpyxl`_       same as above
   `pyexcel-ods3`_          ods                     `pyexcel-ezodf`_, 2.6, 2.7, 3.3, 3.4
                                                    lxml              3.5, 3.6
   `pyexcel-ods`_           ods                     `odfpy`_          same as above
   ======================== ======================= ================= ==================

.. table:: Dedicated file reader and writers

   ======================== ======================= ================= ==================
   Package name              Supported file formats  Dependencies     Python versions
   ======================== ======================= ================= ==================
   `pyexcel-xlsxw`_         xlsx(write only)        `XlsxWriter`_     Python 2 and 3
   `pyexcel-xlsxr`_         xlsx(read only)         lxml              same as above
   `pyexcel-xlsbr`_         xlsx(read only)         pyxlsb            same as above
   `pyexcel-odsr`_          read only for ods, fods lxml              same as above
   `pyexcel-odsw`_          write only for ods      loxun             same as above
   `pyexcel-htmlr`_         html(read only)         lxml,html5lib     same as above
   `pyexcel-pdfr`_          pdf(read only)          pdftables         Python 2 only.
   ======================== ======================= ================= ==================


.. _pyexcel-io: https://github.com/pyexcel/pyexcel-io
.. _pyexcel-xls: https://github.com/pyexcel/pyexcel-xls
.. _pyexcel-xlsx: https://github.com/pyexcel/pyexcel-xlsx
.. _pyexcel-ods: https://github.com/pyexcel/pyexcel-ods
.. _pyexcel-ods3: https://github.com/pyexcel/pyexcel-ods3
.. _pyexcel-odsr: https://github.com/pyexcel/pyexcel-odsr
.. _pyexcel-odsw: https://github.com/pyexcel/pyexcel-odsw
.. _pyexcel-pdfr: https://github.com/pyexcel/pyexcel-pdfr

.. _pyexcel-xlsxw: https://github.com/pyexcel/pyexcel-xlsxw
.. _pyexcel-xlsxr: https://github.com/pyexcel/pyexcel-xlsxr
.. _pyexcel-xlsbr: https://github.com/pyexcel/pyexcel-xlsbr
.. _pyexcel-htmlr: https://github.com/pyexcel/pyexcel-htmlr

.. _xlrd: https://github.com/python-excel/xlrd
.. _xlwt: https://github.com/python-excel/xlwt
.. _openpyxl: https://bitbucket.org/openpyxl/openpyxl
.. _XlsxWriter: https://github.com/jmcnamara/XlsxWriter
.. _pyexcel-ezodf: https://github.com/pyexcel/pyexcel-ezodf
.. _odfpy: https://github.com/eea/odfpy


In order to manage the list of plugins installed, you need to use pip to add or remove
a plugin. When you use virtualenv, you can have different plugins per virtual
environment. In the situation where you have multiple plugins that does the same thing
in your environment, you need to tell pyexcel which plugin to use per function call.
For example, pyexcel-ods and pyexcel-odsr, and you want to get_array to use pyexcel-odsr.
You need to append get_array(..., library='pyexcel-odsr').

.. rubric:: Footnotes

.. [#f1] zipped csv file
.. [#f2] zipped tsv file

After that, you can start get and save data in the loaded format. There
are two plugins for the same file format, e.g. pyexcel-ods3 and pyexcel-ods.
If you want to choose one, please try pip uninstall the un-wanted one. And if
you want to have both installed but wanted to use one of them for a function
call(or file type) and the other for another function call(or file type), you can
pass on "library" option to get_data and save_data, e.g.
get_data(.., library='pyexcel-ods')


.. note::
   pyexcel-text is no longer a plugin of pyexcel-io but a direct plugin of pyexcel


.. table:: Plugin compatibility table

    ============= ======= ======== ======= ======== ======== ========
    `pyexcel-io`_ `xls`_  `xlsx`_  `ods`_  `ods3`_  `odsr`_  `xlsxw`_
    ============= ======= ======== ======= ======== ======== ========
    0.5.10+       0.5.0+  0.5.0+   0.5.4   0.5.3    0.5.0+   0.5.0+
    0.5.1+        0.5.0+  0.5.0+   0.5.0+  0.5.0+   0.5.0+   0.5.0+
    0.4.x         0.4.x   0.4.x    0.4.x   0.4.x    0.4.x    0.4.x
    0.3.0+        0.3.0+  0.3.0    0.3.0+  0.3.0+   0.3.0    0.3.0
    0.2.2+        0.2.2+  0.2.2+   0.2.1+  0.2.1+            0.0.1
    0.2.0+        0.2.0+  0.2.0+   0.2.0   0.2.0             0.0.1
    ============= ======= ======== ======= ======== ======== ========

.. _pyexcel-io: https://github.com/pyexcel/pyexcel-io
.. _xls: https://github.com/pyexcel/pyexcel-xls
.. _xlsx: https://github.com/pyexcel/pyexcel-xlsx
.. _xlsxw: https://github.com/pyexcel/pyexcel-xlsxw
.. _odsr: https://github.com/pyexcel/pyexcel-odsr
.. _ods: https://github.com/pyexcel/pyexcel-ods
.. _ods3: https://github.com/pyexcel/pyexcel-ods3


.. toctree::
   :caption: Migration Note
   :maxdepth: 2

   pyinstaller

.. toctree::
   :caption: Tutorial
   :maxdepth: 2

   plaincsv
   pagination
   renderer
   extendedcsv
   csvz
   sqlalchemy
   django
   extensions


API
--------------------------------------------------

.. toctree::
   :maxdepth: 2

   common_parameters

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
