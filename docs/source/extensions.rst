Extend pyexcel-io Tutorial
================================================================================

pyexcel-io itself comes with csv support.

Reader
--------------------------------------------------------------------------------

Suppose we have a yaml file, containing a dictionary where the values are
two dimensional array. The task is write reader plugin to pyexcel-io so that
we can use get_data() to read it out.

Example yaml data::

    sheet 1:
    - - 1
      - 2
      - 3
    - - 2
      - 3
      - 4
    sheet 2:
    - - A
      - B
      - C
  
Example code::

  import yaml
  from pyexcel_io.sheet import NamedContent
  from pyexcel_io.plugin_api import ISheet
  from pyexcel_io.plugin_api import IReader
  

  class YourSingleSheet(ISheet):
      def __init__(self, your_choice, **your_keywords):
          pass

      def row_iterator(self):
          pass

      def column_iterator(self):
          pass

      def close(self):
          pass


  class YourReader(IReader):
      def __init__(self, file_name, file_type, **keywords):
          # construct self.content_array and should a list of NamedContent
          self.file_handle = open(file_name, 'r')
          self.native_book = yaml.load(self.file_handle)
          self.content_array = [NamedContent(key, values) for key, values in self.native_book.items()]

      def read_sheet(self, sheet_index):
          pass

      def close():
          pass

Writer
--------------------------------------------------------------------------------



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
