Read partial data
================================================================================

When you are dealing with huge amount of data, obviously you would not like to
fill up your memory with those data. Here is a the feature to support pagination
of your data.

.. testcode::
   :hide:

    >>> import sys
    >>> if sys.version_info[0] < 3:
    ...     from StringIO import StringIO
    ... else:
    ...     from io import StringIO
    >>> from pyexcel_io._compact import OrderedDict

Let's assume the following file is a huge csv file:

.. code-block:: python

   >>> import datetime
   >>> from pyexcel_io import save_data
   >>> data = [
   ...     [1, 21, 31],
   ...     [2, 22, 32],
   ...     [3, 23, 33],
   ...     [4, 24, 34],
   ...     [5, 25, 35],
   ...     [6, 26, 36]
   ... ]
   >>> save_data("your_file.csv", data)

And let's pretend to read partial data:

.. code-block:: python

   >>> from pyexcel_io import get_data
   >>> data = get_data("your_file.csv", start_row=2, row_limit=3)
   >>> data['your_file.csv']
   [[3, 23, 33], [4, 24, 34], [5, 25, 35]]

And you could as well do the same for columns:

.. code-block:: python

   >>> data = get_data("your_file.csv", start_column=1, column_limit=2)
   >>> data['your_file.csv']
   [[21, 31], [22, 32], [23, 33], [24, 34], [25, 35], [26, 36]]

Obvious, you could do both at the same time:

.. code-block:: python

   >>> data = get_data("your_file.csv",
   ...     start_row=2, row_limit=3,
   ...     start_column=1, column_limit=2)
   >>> data['your_file.csv']
   [[23, 33], [24, 34], [25, 35]]

The pagination support is available across all pyexcel-io plugins.

