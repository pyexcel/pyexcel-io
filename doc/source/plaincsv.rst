Working with CSV format
================================================================================

As a standalone library
------------------------

Write to a csv file
*********************

.. testcode::
   :hide:

    >>> import sys
    >>> if sys.version_info[0] < 3:
    ...     from StringIO import StringIO
    ... else:
    ...     from io import BytesIO as StringIO
    >>> from pyexcel_io import OrderedDict


Here's the sample code to write a dictionary to a csv file::

    >>> from pyexcel_io import store_data
    >>> data = OrderedDict() # from collections import OrderedDict
    >>> data.update({"Sheet 1": [[1, 2, 3], [4, 5, 6]]})
    >>> data.update({"Sheet 2": [["row 1", "row 2", "row 3"]]})
    >>> store_data("your_file.csv", data)

Read from a csv file
**********************

Here's the sample code::

    >>> from pyexcel_io import load_data
    >>> data = load_data("your_file.csv")
    >>> import json
    >>> print(json.dumps(data))
    {"Sheet 1": [["1", "2", "3"], ["4", "5", "6"]], "Sheet 2": [["row 1", "row 2", "row 3"]]}

Write a csv to memory
**********************

Here's the sample code to write a dictionary as a csv into memory::

    >>> from pyexcel_io import store_data
    >>> data = OrderedDict()
    >>> data.update({"Sheet 1": [[1, 2, 3], [4, 5, 6]]})
    >>> data.update({"Sheet 2": [[7, 8, 9], [10, 11, 12]]})
    >>> io = StringIO()
    >>> store_data(io, data)
    >>> # do something with the io
    >>> # In reality, you might give it to your http response
    >>> # object for downloading

    
Read from a csv from memory
*****************************

Continue from previous example::

    >>> # This is just an illustration
    >>> # In reality, you might deal with csv file upload
    >>> # where you will read from requests.FILES['YOUR_XL_FILE']
    >>> data = load_data(io)
    >>> print(json.dumps(data))
    {"Sheet 1": [[1, 2, 3], [4, 5, 6]], "Sheet 2": [[7, 8, 9], [10, 11, 12]]}


As a pyexcel plugin
--------------------

Import it in your file to enable this plugin::

    from pyexcel.ext import io

Please note only pyexcel version 0.0.4+ support this.

Reading from a csv file
************************

Here is the sample code::

    >>> import pyexcel as pe
    >>> from pyexcel.ext import io
    >>> sheet = pe.get_book(file_name="your_file.csv")
    >>> sheet
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

Writing to a csv file
**********************

Here is the sample code::

    >>> sheet.save_as("another_file.csv")

Reading from a IO instance
================================

You got to wrap the binary content with stream to get csv working::

    >>> # This is just an illustration
    >>> # In reality, you might deal with csv file upload
    >>> # where you will read from requests.FILES['YOUR_CSV_FILE']
    >>> csvfile = "another_file.csv"
    >>> with open(csvfile, "rb") as f:
    ...     content = f.read()
    ...     r = pe.get_book(file_type="csv", file_content=content)
    ...     print(r)
    ...
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


Writing to a StringIO instance
================================

You need to pass a StringIO instance to Writer::

    >>> data = [
    ...     [1, 2, 3],
    ...     [4, 5, 6]
    ... ]
    >>> io = StringIO()
    >>> sheet = pe.Sheet(data)
    >>> sheet.save_to_memory("csv", io)
    >>> # then do something with io
    >>> # In reality, you might give it to your http response
    >>> # object for downloading
