Saving multiple sheets as CSV format
================================================================================

.. testcode::
   :hide:

    >>> from pyexcel_io._compact import OrderedDict, StringIO


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
    {"Sheet 1": [[1, 2, 3], [4, 5, 6]], "Sheet 2": [["row 1", "row 2", "row 3"]]}

Here is what you would get::

    >>> import glob
    >>> list = glob.glob("your_file__*.csv")
    >>> json.dumps(sorted(list))
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
    >>> save_data(io, data)
    >>> # do something with the io
    >>> # In reality, you might give it to your http response
    >>> # object for downloading

    
Read multiple sibling csv files from memory
--------------------------------------------------------------------------------

Continue from previous example::

    >>> # This is just an illustration
    >>> # In reality, you might deal with csv file upload
    >>> # where you will read from requests.FILES['YOUR_XL_FILE']
    >>> data = get_data(io, multiple_sheets=True)
    >>> print(json.dumps(data))
    {"Sheet 1": [[1, 2, 3], [4, 5, 6]], "Sheet 2": [[7, 8, 9], [10, 11, 12]]}


.. testcode::
   :hide:

   >>> import os
   >>> os.unlink("your_file__Sheet 1__0.csv")
   >>> os.unlink("your_file__Sheet 2__1.csv")
   
