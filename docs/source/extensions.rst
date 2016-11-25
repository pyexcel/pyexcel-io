Working with xls, xlsx, and ods formats
================================================================================

.. note::

   No longer, you will need to do explicit imports for pyexcel-io extensions.
   Instead, you install them and manage them via pip.

Work with physical file
-----------------------------------------------------------------------------

Here's what is needed::

    >>> from pyexcel_io import save_data
    >>> data = [[1,2,3]]
    >>> save_data("test.xls", data)

And you can also get the data back::

    >>> from pyexcel_io import get_data
    >>> data = get_data("test.xls")
    >>> data['pyexcel_sheet1']
    [[1, 2, 3]]


Work with memory file
-----------------------------------------------------------------------------

Here is the sample code to work with memory file::

    >>> from pyexcel_io.manager import get_io
    >>> io = get_io("xls")
    >>> data = [[1,2,3]]
    >>> save_data(io, data, "xls")

The difference is that you have mention file type if you use :meth:`pyexcel_io.save_data`

And you can also get the data back::

    >>> data = get_data(io, "xls") 
    >>> data['pyexcel_sheet1']
    [[1, 2, 3]]

The same applies to :meth:`pyexcel_io.get_data`.


Other formats
-----------------------------------------------------------------------------

As illustrated above, you can start to play with pyexcel-xlsx, pyexcel-ods and
pyexcel-ods3 plugins.

.. testcode::
   :hide:

   >>> import os
   >>> os.unlink("test.xls")
