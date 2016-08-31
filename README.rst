================================================================================
pyexcel-io - Let you focus on data, instead of file formats
================================================================================

.. image:: https://api.travis-ci.org/pyexcel/pyexcel-io.svg?branch=master
   :target: http://travis-ci.org/pyexcel/pyexcel-io

.. image:: https://codecov.io/github/pyexcel/pyexcel-io/coverage.png
    :target: https://codecov.io/github/pyexcel/pyexcel-io

.. image:: https://readthedocs.org/projects/pyexcel-io/badge/?version=latest
   :target: http://pyexcel-io.readthedocs.org/en/latest/


**pyexcel-io** provides **one** application programming interface(API) to read
and write the data in excel format, import the data into and export the data
from database. It provides support for csv(z) format, django database and
sqlalchemy supported databases. Its supported file formats are extended to cover
"xls", "xlsx", "ods" by the following extensions:

.. _file-format-list:
.. _a-map-of-plugins-and-file-formats:

.. table:: A list of file formats supported by external plugins

   ================= ======================= ============= ==================
   Package name      Supported file formats  Dependencies  Python versions
   ================= ======================= ============= ==================
   `pyexcel-io`_     csv, csvz [#f1]_, tsv,                2.6, 2.7, 3.3,
                                                           3.4, pypy, pypy3
                     tsvz [#f2]_
   `pyexcel-xls`_    xls, xlsx(read only),   xlrd, xlwt    2.6, 2.7, 3.3,
                                                           3.4, pypy, pypy3
                     xlsm(read only)
   `pyexcel-xlsx`_   xlsx                    openpyxl      2.6, 2.7, 3.3,
                                                           3.4, pypy, pypy3
   `pyexcel-xlsxw`_  xlsx(write only)        xlsxwriter    2.6, 2.7, 3.3,
                                                           3.4, pypy, pypy3
   `pyexcel-ods3`_   ods                     ezodf, lxml   2.6, 2.7, 3.3, 3.4
   `pyexcel-ods`_    ods (python 2.6, 2.7)   odfpy         2.6, 2.7, 3.3, 3.4
   ================= ======================= ============= ==================

.. _pyexcel-io: https://github.com/pyexcel/pyexcel-io
.. _pyexcel-xls: https://github.com/pyexcel/pyexcel-xls
.. _pyexcel-xlsx: https://github.com/pyexcel/pyexcel-xlsx
.. _pyexcel-ods: https://github.com/pyexcel/pyexcel-ods
.. _pyexcel-ods3: https://github.com/pyexcel/pyexcel-ods3
.. _pyexcel-xlsxw: https://github.com/pyexcel/pyexcel-xlsxw

.. rubric:: Footnotes

.. [#f1] zipped csv file
.. [#f2] zipped tsv file

If you need to manipulate the data, you might do it yourself or use its brother
library `pyexcel <https://github.com/pyexcel/pyexcel>`__ .

If you would like to extend it, you may use it to write your own
extension to handle a specific file format.


Known constraints
==================

Fonts, colors and charts are not supported.


Installation
================================================================================
You can install it via pip:

.. code-block:: bash

    $ pip install pyexcel-io


or clone it and install it:

.. code-block:: bash

    $ git clone http://github.com/pyexcel/pyexcel-io.git
    $ cd pyexcel-io
    $ python setup.py install



License
================================================================================

New BSD License
