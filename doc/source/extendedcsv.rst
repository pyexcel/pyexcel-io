Saving multiple sheets as CSV format
================================================================================

.. testcode::
   :hide:

    >>> import sys
    >>> if sys.version_info[0] < 3:
    ...     from StringIO import StringIO
    ... else:
    ...     from io import BytesIO as StringIO
    >>> from pyexcel_io import OrderedDict


Write to multiple sibling csv files
------------------------------------------------------------------------------


Here's the sample code to write a dictionary to multiple sibling csv files::

    >>> from pyexcel_io import save_data
    >>> data = OrderedDict() # from collections import OrderedDict
    >>> data.update({"Sheet 1": [[1, 2, 3], [4, 5, 6]]})
    >>> data.update({"Sheet 2": [["row 1", "row 2", "row 3"]]})
    >>> save_data("your_file.csv", data)


Read from multiple sibling csv files
--------------------------------------------------------------------------------


Here's the sample code::

    >>> from pyexcel_io import get_data
    >>> data = get_data("your_file.csv")
    >>> import json
    >>> print(json.dumps(data))
    {"Sheet 1": [["1", "2", "3"], ["4", "5", "6"]], "Sheet 2": [["row 1", "row 2", "row 3"]]}

Here is what you would get::

    >>> import glob
    >>> list = glob.glob("your_file__*.csv")
    >>> json.dumps(list)
    '["your_file__Sheet 1__0.csv", "your_file__Sheet 2__1.csv"]'
    

Write multiple sibling csv files  to memory
--------------------------------------------------------------------------------

Here's the sample code to write a dictionary of named two dimensional array
into memory::

    >>> from pyexcel_io import save_data
    >>> data = OrderedDict()
    >>> data.update({"Sheet 1": [[1, 2, 3], [4, 5, 6]]})
    >>> data.update({"Sheet 2": [[7, 8, 9], [10, 11, 12]]})
    >>> io = StringIO()
    >>> save_data(io, data, 'csv')
    >>> # do something with the io
    >>> # In reality, you might give it to your http response
    >>> # object for downloading

    
Read multiple sibling csv files from memory
--------------------------------------------------------------------------------

Continue from previous example::

    >>> # This is just an illustration
    >>> # In reality, you might deal with csv file upload
    >>> # where you will read from requests.FILES['YOUR_XL_FILE']
    >>> data = get_data(io)
    >>> print(json.dumps(data))
    {"Sheet 1": [["1", "2", "3"], ["4", "5", "6"]], "Sheet 2": [["7", "8", "9"], ["10", "11", "12"]]}


As a pyexcel plugin
------------------------------------------------------------------------------


Reading from multiple sibling csv files
********************************************************************************

Here is the sample code::

    >>> import pyexcel as pe
    >>> from pyexcel.ext import io
    >>> book = pe.get_book(file_name="your_file.csv")
    >>> book
    Sheet Name: Sheet 1
    +---+---+---+
    | 1 | 2 | 3 |
    +---+---+---+
    | 4 | 5 | 6 |
    +---+---+---+
    Sheet Name: Sheet 2
    +-------+-------+-------+
    | row 1 | row 2 | row 3 |
    +-------+-------+-------+

Writing to multiple sibling csv files
********************************************************************************

Here is the sample code::

    >>> book.save_as("another_file.csv")


Writing multiple sibling csv files to a StringIO instance
********************************************************************************

You need to pass a StringIO instance to Writer::

    >>> io = StringIO()
    >>> book.save_to_memory("csv", io)
    >>> # then do something with io
    >>> # In reality, you might give it to your http response
    >>> # object for downloading


Reading multiple sibling csv files from a IO instance
********************************************************************************

You got to wrap the binary content with stream to get csv working::

    >>> # This is just an illustration
    >>> # In reality, you might deal with csv file upload
    >>> # where you will read from requests.FILES['YOUR_CSV_FILE']
    >>> memory_book = pe.get_book(file_type="csv", file_stream=io)
    >>> memory_book
    Sheet Name: Sheet 1
    +---+---+---+
    | 1 | 2 | 3 |
    +---+---+---+
    | 4 | 5 | 6 |
    +---+---+---+
    Sheet Name: Sheet 2
    +-------+-------+-------+
    | row 1 | row 2 | row 3 |
    +-------+-------+-------+


.. testcode::
   :hide:

   >>> import os
   >>> os.unlink("your_file__Sheet 1__0.csv")
   >>> os.unlink("your_file__Sheet 2__1.csv")
   >>> os.unlink("another_file__Sheet 1__0.csv")
   >>> os.unlink("another_file__Sheet 2__1.csv")
   
