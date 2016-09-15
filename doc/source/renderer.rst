Rendering(Formatting) the data

================================================================================

You might want to do custom rendering on your data obtained. `row_renderer` was
added since version 0.2.3. Here is how you can use it.

.. testcode::
   :hide:

    >>> import sys
    >>> if sys.version_info[0] < 3:
    ...     from StringIO import StringIO
    ... else:
    ...     from io import StringIO
    >>> from pyexcel_io._compact import OrderedDict

Let's assume the following file:

.. code-block:: python

   >>> import datetime
   >>> from pyexcel_io import save_data
   >>> data = [
   ...     [1, 21, 31],
   ...     [2, 22, 32],
   ...     [3, 23, 33]
   ... ]
   >>> save_data("your_file.csv", data)

And let's read them back:

.. code-block:: python

   >>> from pyexcel_io import get_data
   >>> data = get_data("your_file.csv")
   >>> data['your_file.csv']
   [[1, 21, 31], [2, 22, 32], [3, 23, 33]]

And you may want use row_renderer to customize it to string:

.. code-block:: python

   >>> def my_renderer(row):
   ...     return [str(element) for element in row]
   >>> data = get_data("your_file.csv", row_renderer=my_renderer)
   >>> data['your_file.csv']
   [['1', '21', '31'], ['2', '22', '32'], ['3', '23', '33']]
