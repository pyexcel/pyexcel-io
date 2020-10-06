Extend pyexcel-io Tutorial
================================================================================

You are welcome to extend pyexcel-io to read and write more tabular formats.
No. 1 rule, your plugin must have a prefix 'pyexcel_' in its module path.
For example, `pyexcel-xls` has 'pyexcel_xls' as its module path. Otherwise,
pyexcel-io will not load your plugin.

On github, you will find two examples in `examples` folder. This section
explains its implementations to help you write yours.

.. note::

   No longer, you will need to do explicit imports for pyexcel-io extensions.
   Instead, you install them and manage them via pip.

Simple Reader for a yaml file
--------------------------------------------------------------------------------

Suppose we have a yaml file, containing a dictionary where the values are
two dimensional array. The task is to write a reader plugin to pyexcel-io so that
we can use get_data() to read yaml file out.

.. literalinclude:: ../../examples/test.yaml
  :language: yaml

**Implement IReader**

First, let's impolement reader interface as below. Three implementations are required:

1. `content_array` attribute, is expected to be a list of `NamedContent`
2. `read_sheet` function, read sheet content by its index.
3. `close` function, to clean up any file handle

.. literalinclude:: ../../examples/custom_yaml_reader.py
  :language: python
  :lines: 19-33

**Implement ISheet**

`YourSingleSheet` makes this simple task complex in order to show case its inner
workings. Two abstract functions require implementation:

1. `row_iterator`: should return a row: either content arry or content index as long as
                   `column_iterator` understands

2. `column_iterator`: should return cell values one by one.

.. literalinclude:: ../../examples/custom_yaml_reader.py
  :language: python
  :lines: 8-16


**Plug in pyexcel-io**

Last thing is to register with pyexcel-io about your new reader. `relative_plugin_class_path`
meant reference from current module, how to refer to `YourReader`. `locations` meant
the physical presence of the data source: "file", "memory" or "content". "file" means
files on physical disk. "memory" means a file stream. "content" means a string buffer.
`stream_type` meant the type of the stream: binary for BytesIO and text for StringIO.

.. literalinclude:: ../../examples/custom_yaml_reader.py
  :language: python
  :lines: 36-41


**Test your reader**

Let's run the following code and see if it works.

.. literalinclude:: ../../examples/custom_yaml_reader.py
  :language: python
  :lines: 43-45


You would see these in standard output:

.. code-block:: bash

   $ python custom_yaml_reader.py
   OrderedDict([('sheet 1', [[1, 2, 3], [2, 3, 4]]), ('sheet 2', [['A', 'B', 'C']])])                

A writer to write content in yaml
--------------------------------------------------------------------------------

Now for the writer, let's write a pyexcel-io writer that write a dictionary of
two dimentaional arrays back into a yaml file seen above.

**Implement IWriter**

Two abstract functions are required:

1. `create_sheet` creates a native sheet by sheet name, that understands how to code up the native sheet. Interestingly, it returns your sheet.
2. `close` function closes file handle if any.

.. literalinclude:: ../../examples/custom_yaml_writer.py
  :language: python
  :lines: 18-30

**Implement ISheetWriter**

It is imagined that you will have your own sheet writer. You simply need to figure
out how to write a row. Row by row write action was already written by `ISheetWrier`.


.. literalinclude:: ../../examples/custom_yaml_writer.py
  :language: python
  :lines: 7-14

**Plug in pyexcel-io**

Like the reader plugin, we register a writer.

.. literalinclude:: ../../examples/custom_yaml_writer.py
  :language: python
  :lines: 33-38

**Test It**

Let's run the following code and please examine `mytest.yaml` yourself.

.. literalinclude:: ../../examples/custom_yaml_writer.py
  :language: python
  :lines: 40-46

And you shall find a file named 'mytest.yaml':


.. code-block:: bash

   $ cat mytest.yaml
   sheet 1:
   - - 1
     - 3
     - 4
   - - 2
     - 4
     - 9
   sheet 2:
   - - B
     - C
     - D


Other pyexcel-io plugins
-----------------------------------------------------------------------------

Get xls support

.. code-block::


   $ pip install pyexcel-xls


Here's what is needed::

    >>> from pyexcel_io import save_data
    >>> data = [[1,2,3]]
    >>> save_data("test.xls", data)

And you can also get the data back::

    >>> from pyexcel_io import get_data
    >>> data = get_data("test.xls")
    >>> data['pyexcel_sheet1']
    [[1, 2, 3]]


Other formats
-----------------------------------------------------------------------------

As illustrated above, you can start to play with pyexcel-xlsx, pyexcel-ods and
pyexcel-ods3 plugins.

.. testcode::
   :hide:

   >>> import os
   >>> os.unlink("test.xls")
