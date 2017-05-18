Working with CSV format
================================================================================

Please note that csv reader load data in a lazy manner. It ignores excessive
trailing cells that has None value. For example, the following csv content::

    1,2,,,,,
    3,4,,,,,
    5,,,,,,,

would end up as::

    1,2
    3,4
    5,

Write to a csv file
--------------------------------------------------------------------------------

.. testcode::
   :hide:

    >>> import sys
    >>> if sys.version_info[0] < 3:
    ...     from StringIO import StringIO
    ... else:
    ...     from io import StringIO
    >>> from pyexcel_io._compact import OrderedDict

Here's the sample code to write an array to a csv file ::

   >>> import datetime
   >>> from pyexcel_io import save_data
   >>> data = [
   ...     [1, 2.0, 3.0],
   ...     [
   ...         datetime.date(2016, 5, 4),
   ...         datetime.datetime(2016, 5, 4, 17, 39, 12),
   ...         datetime.datetime(2016, 5, 4, 17, 40, 12, 100)
   ...     ]
   ... ]
   >>> save_data("your_file.csv", data)

Let's verify the file content::

   >>> with open("your_file.csv", "r") as csvfile:
   ...     for line in csvfile.readlines():
   ...         print(line.strip())
   1,2.0,3.0
   2016-05-04,2016-05-04 17:39:12,2016-05-04 17:40:12.000100


Change line endings
*************************

By default, python csv module provides windows line ending '\r\n'. In order
to change it, you can do:
   
   >>> save_data("your_file.csv", data, lineterminator='\n')

Read from a csv file
--------------------------------------------------------------------------------

And we can read the written csv file back as the following code::

    >>> from pyexcel_io import get_data
    >>> import pprint
    >>> data = get_data("your_file.csv")
    >>> pprint.pprint(data['your_file.csv'])
    [[1, 2.0, 3.0],
     [datetime.date(2016, 5, 4),
      datetime.datetime(2016, 5, 4, 17, 39, 12),
      datetime.datetime(2016, 5, 4, 17, 40, 12, 100)]]

As you can see, pyexcel-io not only reads the csv file back but also
recognizes the data types: `int`, `float`, `date` and `datetime`. However, it
does give your cpu some extra job. When you are handling a large csv file and
the cpu budget is of your concern, you may switch off the type detection feature.
For example, let's switch all off:
  
    >>> data = get_data("your_file.csv", auto_detect_float=False, auto_detect_datetime=False)
	>>> import json
    >>> json.dumps(data['your_file.csv'])
    '[[1, "2.0", "3.0"], ["2016-05-04", "2016-05-04 17:39:12", "2016-05-04 17:40:12.000100"]]'

In addition to `auto_detect_float` and `auto_detect_datetime`, there is another flag named `auto_detect_int`, which becomes active only if `auto_detect_float` is `True`. Now, let's play a bit with `auto_detect_int`:

    >>> data = get_data("your_file.csv", auto_detect_int=False)
    >>> pprint.pprint(data['your_file.csv'])
    [[1.0, 2.0, 3.0],
     [datetime.date(2016, 5, 4),
      datetime.datetime(2016, 5, 4, 17, 39, 12),
      datetime.datetime(2016, 5, 4, 17, 40, 12, 100)]]

As you see, all numeric data are identified as float type. If you looked a few paragraphs above, you would notice `auto_detect_int` affected [1, 2, ..] in the first row.

Write a csv to memory
--------------------------------------------------------------------------------

Here's the sample code to write a dictionary as a csv into memory::

    >>> from pyexcel_io import save_data
    >>> data = [[1, 2, 3], [4, 5, 6]]
    >>> io = StringIO()
    >>> save_data(io, data)
    >>> # do something with the io
    >>> # In reality, you might give it to your http response
    >>> # object for downloading

    
Read from a csv from memory
--------------------------------------------------------------------------------

Continue from previous example:

    >>> # This is just an illustration
    >>> # In reality, you might deal with csv file upload
    >>> # where you will read from requests.FILES['YOUR_XL_FILE']
    >>> import json
    >>> data = get_data(io)
    >>> print(json.dumps(data))
    {"csv": [[1, 2, 3], [4, 5, 6]]}


Encoding parameter
--------------------------------------------------------------------------------

In general, if you would like to save your csv file into a custom encoding, you
can specify 'encoding' parameter. Here is how you write verses of
a finnish song, "Aurinko laskee länteen"[#f1]_ into a csv file

.. code-block:: python

    >>> content = [[u'Aurinko laskee länteen', u'Näin sen ja ymmärsin sen', u'Poissa aika on rakkauden Kun aurinko laskee länteen']]
    >>> test_file = "test-utf16-encoding.csv"
	>>> save_data(test_file, content, encoding="utf-16", lineterminator="\n")

In the reverse direction, if you would like to read your csv file with custom
encoding back, you do the same to get_data:

.. code-block:: python

    >>> custom_encoded_content = get_data(test_file, encoding="utf-16")
	>>> assert custom_encoded_content[test_file] == content

.. [#f1] A finnish song that was entered in Eurovision in 1965. You can check out its lyrics at `diggiloo.net <http://www.diggiloo.net/?1965fi>`_

Byte order mark (BOM) in csv file
--------------------------------------------------------------------------------

By passing **encoding="utf-8-sig", You can write UTF-8 BOM header into your csv file.
Here is an example to write a sentence of "Shui Dial Getou"[#f2] into a csv file:

.. code-block:: python

    >>> content = [[u'人有悲歡離合', u'月有陰晴圓缺']]
    >>> test_file = "test-utf8-BOM.csv"
	>>> save_data(test_file, content, encoding="utf-8-sig", lineterminator="\n")

When you read it back you will have to specify encoding too.

.. code-block:: python

    >>> custom_encoded_content = get_data(test_file, encoding="utf-8-sig")
	>>> assert custom_encoded_content[test_file] == content


.. [#f2] One of Su shi's most famous poem. Here is the `wiki link <https://en.wikipedia.org/wiki/Shuidiao_Getou>`_

.. testcode::
   :hide:

   >>> import os
   >>> os.unlink("your_file.csv")
   >>> os.unlink(test_file)
