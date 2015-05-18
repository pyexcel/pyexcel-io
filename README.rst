================================================================================
pyexcel-io - Let you focus on data, instead of file formats
================================================================================

.. image:: https://api.travis-ci.org/chfw/pyexcel-io.png
    :target: http://travis-ci.org/chfw/pyexcel-io

.. image:: https://coveralls.io/repos/chfw/pyexcel-io/badge.png?branch=master 
    :target: https://coveralls.io/r/chfw/pyexcel-io?branch=master 

.. image:: https://readthedocs.org/projects/pyexcel-io/badge/?version=latest
    :target: http://pyexcel-io.readthedocs.org/en/latest/

.. image:: http://img.shields.io/gittip/chfw.svg
    :target: https://gratipay.com/chfw/

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
`pyexcel-ods`_   ods (python 2.6, 2.7 only)        
`pyexcel-ods3`_  ods
================ ==================================

.. _pyexcel-xls: https://github.com/chfw/pyexcel-xls
.. _pyexcel-xlsx: https://github.com/chfw/pyexcel-xlsx
.. _pyexcel-ods: https://github.com/chfw/pyexcel-ods
.. _pyexcel-ods3: https://github.com/chfw/pyexcel-ods3

If you need to manipulate the data, you might do it yourself or use its brother
library `pyexcel <https://github.com/chfw/pyexcel>`__ .

If you would like to extend it, you may use it to write your own
extension to handle a specific file format.

Known constraints
================================================================================

Fonts, colors and charts are not supported. 


Installation
================================================================================


You can install it via pip::

    $ pip install pyexcel-io


or clone it and install it::

    $ git clone http://github.com/chfw/pyexcel-io.git
    $ cd pyexcel-io
    $ python setup.py install


License
===========

New BSD License


Dependencies
============

1. python 2.6, orderreddict
