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

**pyexcel-io** is a tiny wrapper library to read and write the data in csv format,
import the data into and export the data from database. If you need to manipulate
the data, you might use its brother library
`pyexcel <https://github.com/chfw/pyexcel>`__ .

Meanwhile, if you would like to extend it, you may use it to write your own
extension to handle a specific file format: reading content from and writing
content to.


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
