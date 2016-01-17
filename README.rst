================================================================================
pyexcel-io - Let you focus on data, instead of file formats
================================================================================

.. image:: https://api.travis-ci.org/pyexcel/pyexcel-io.png
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

================ ==================================
Plugins          Supported file formats            
================ ==================================
`pyexcel-xls`_   xls, xlsx(r), xlsm(r)
`pyexcel-xlsx`_  xlsx
`pyexcel-ods3`_  ods
`pyexcel-ods`_   ods (python 2.6, 2.7 only)        
================ ==================================

.. _pyexcel-xls: https://github.com/pyexcel/pyexcel-xls
.. _pyexcel-xlsx: https://github.com/pyexcel/pyexcel-xlsx
.. _pyexcel-ods: https://github.com/pyexcel/pyexcel-ods
.. _pyexcel-ods3: https://github.com/pyexcel/pyexcel-ods3

If you need to manipulate the data, you might do it yourself or use its brother
library `pyexcel <https://github.com/pyexcel/pyexcel>`__ .

If you would like to extend it, you may use it to write your own
extension to handle a specific file format.

Features to be released
================================================================================

Yield the data reading until it is actually used. This action may potentially
speed up file format transcoding and reduce the demand for run-time memory. This
may enable web content stream too.


Known constraints
================================================================================

Fonts, colors and charts are not supported. 


Installation
================================================================================


You can install it via pip::

    $ pip install pyexcel-io


or clone it and install it::

    $ git clone http://github.com/pyexcel/pyexcel-io.git
    $ cd pyexcel-io
    $ python setup.py install


License
===========

New BSD License


Dependencies
============

1. python 2.6, orderreddict
