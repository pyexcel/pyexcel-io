Working with django database
================================================================================

.. testcode::
   :hide:

    >>> class Attributable:
    ...     def __init__(self, adict):
    ...         self.mydict = adict
    ...         
    ...     def __getattr__(self, field):
    ...         return self.mydict[field]
    ... 
    >>> class Objects:
    ...     def __init__(self):
    ...         self.objs = None
    ...         
    ...     def bulk_create(self, objs, batch_size):
    ...         self.objs = objs
    ...         self.batch_size = batch_size
    ... 
    ...     def all(self):
    ...         return [Attributable(o) for o in self.objs]
    ... 
    >>> class Field:
    ...     def __init__(self, name):
    ...         self.attname = name
    ... 
    >>> class Meta:
    ...     instance = 0
    ...     def __init__(self):
    ...         self.model_name = "Sheet%d" % Meta.instance
    ...         self.concrete_fields = []
    ...         Meta.instance = Meta.instance + 1
    ... 
    ...     def update(self, data):
    ...         for f in data:
    ...             self.concrete_fields.append(Field(f))

This section shows the way to to write and read from django database. Becuase it
is "heavy"" to include a django site here to show you. A mocked django model is
used here to demonstate it::

    >>> class FakeDjangoModel:
    ...     def __init__(self):
    ...         self.objects = Objects()
    ...         self._meta = Meta()
    ... 
    ...     def __call__(self, **keywords):
    ...         return keywords

.. note::
   You can visit
   `django-excel documentation <http://django-excel.readthedocs.org/en/latest/>`_
   if you would prefer a real django model to be used in tutorial.

Write data to a django model
--------------------------------------------------------------------------------

Let's suppose we have a django model:

    >>> from pyexcel_io import save_data
    >>> from pyexcel_io.constants import DB_DJANGO, DEFAULT_SHEET_NAME
    >>> from pyexcel_io.database.common import DjangoModelImporter, DjangoModelImportAdapter
    >>> from pyexcel_io.database.common import DjangoModelExporter, DjangoModelExportAdapter
    >>> model = FakeDjangoModel()

Suppose you have these data::

    >>> data  = [
    ...     ["X", "Y", "Z"],
    ...     [1, 2, 3],
    ...     [4, 5, 6]
    ... ]
    >>> importer = DjangoModelImporter()
    >>> adapter = DjangoModelImportAdapter(model)
    >>> adapter.column_names = data[0]
    >>> importer.append(adapter)
    >>> save_data(importer, {adapter.get_name(): data[1:]}, file_type=DB_DJANGO)
    >>> import pprint
    >>> pprint.pprint(model.objects.objs)
    [{'X': 1, 'Y': 2, 'Z': 3}, {'X': 4, 'Y': 5, 'Z': 6}]

Read data from a django model
--------------------------------------------------------------------------------

.. testcode::
   :hide:

   >>> model._meta.update(["X", "Y", "Z"])

Continue from previous example, you can read this back::

   >>> from pyexcel_io import get_data
   >>> exporter = DjangoModelExporter()
   >>> adapter = DjangoModelExportAdapter(model)
   >>> exporter.append(adapter)
   >>> data = get_data(exporter, file_type=DB_DJANGO)
   >>> data
   OrderedDict([('Sheet0', [['X', 'Y', 'Z'], [1, 2, 3], [4, 5, 6]])])

Read a sub set of the columns:

   >>> exporter = DjangoModelExporter()
   >>> adapter = DjangoModelExportAdapter(model, ['X'])
   >>> exporter.append(adapter)
   >>> data = get_data(exporter, file_type=DB_DJANGO)
   >>> data
   OrderedDict([('Sheet0', [['X'], [1], [4]])])

Write data into multiple models
--------------------------------------------------------------------------------

Suppose you have the following data to be stored in the database:

    >>> data = {
    ...     "Sheet1": [['X', 'Y', 'Z'], [1, 4, 7], [2, 5, 8], [3, 6, 9]],
    ...     "Sheet2": [['A', 'B', 'C'], [1, 4, 7], [2, 5, 8], [3, 6, 9]]
    ... }

And want to save them to two django models:

    >>> model1 = FakeDjangoModel()
    >>> model2 = FakeDjangoModel()

In order to store a dictionary data structure, you need to do some transformation::

    >>> importer = DjangoModelImporter()
    >>> adapter1 = DjangoModelImportAdapter(model1)
    >>> adapter1.column_names = data['Sheet1'][0]
    >>> adapter2 = DjangoModelImportAdapter(model2)
    >>> adapter2.column_names = data['Sheet2'][0]
    >>> importer.append(adapter1)
    >>> importer.append(adapter2)
    >>> to_store = {
    ...    adapter1.get_name(): data['Sheet1'][1:],
    ...    adapter2.get_name(): data['Sheet2'][1:]
    ... }
    >>> save_data(importer, to_store, file_type=DB_DJANGO)
    >>> pprint.pprint(model1.objects.objs)
    [{'X': 1, 'Y': 4, 'Z': 7}, {'X': 2, 'Y': 5, 'Z': 8}, {'X': 3, 'Y': 6, 'Z': 9}]
    >>> pprint.pprint(model2.objects.objs)
    [{'A': 1, 'B': 4, 'C': 7}, {'A': 2, 'B': 5, 'C': 8}, {'A': 3, 'B': 6, 'C': 9}]

.. testcode:
   :hide:

   >>> model1._meta.update(["X", "Y", "Z"])
   >>> model2._meta.update(["A", "B", "C"])
   
Read content from multiple tables
--------------------------------------------------------------------------------

Here's what you need to do:

    >>> exporter = DjangoModelExporter()
    >>> adapter1 = DjangoModelExportAdapter(model1)
    >>> adapter2 = DjangoModelExportAdapter(model2)
    >>> exporter.append(adapter1)
    >>> exporter.append(adapter2)
    >>> data = get_data(exporter, file_type=DB_DJANGO)
    >>> data
    OrderedDict([('Sheet1', [['X', 'Y', 'Z'], [1, 4, 7], [2, 5, 8], [3, 6, 9]]), ('Sheet2', [['A', 'B', 'C'], [1, 4, 7], [2, 5, 8], [3, 6, 9]])])

What if we need only a subset of each model

    >>> exporter = DjangoModelExporter()
    >>> adapter1 = DjangoModelExportAdapter(model1, ['X'])
    >>> adapter2 = DjangoModelExportAdapter(model2, ['A'])
    >>> exporter.append(adapter1)
    >>> exporter.append(adapter2)
    >>> data = get_data(exporter, file_type=DB_DJANGO)
    >>> data
    OrderedDict([('Sheet1', [['X'], [1], [2], [3]]), ('Sheet2', [['A'], [1], [2], [3]])])
