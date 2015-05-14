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
    ...     def __init__(self):
    ...         self.model_name = "test"
    ...         self.concrete_fields = []
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

Write data to a django model
--------------------------------------------------------------------------------

Let's suppose we have a django model:

    >>> from pyexcel_io import save_data, DB_DJANGO
    >>> model = FakeDjangoModel()

Suppose you have these data::

    >>> data  = [
    ...     ["X", "Y", "Z"],
    ...     [1, 2, 3],
    ...     [4, 5, 6]
    ... ]
    >>> save_data(DB_DJANGO, data[1:], models={"csv": [model, data[0], None, None]})
    >>> model.objects.objs
    [{'Y': 2, 'X': 1, 'Z': 3}, {'Y': 5, 'X': 4, 'Z': 6}]

Read data from a django model
--------------------------------------------------------------------------------

.. testcode::
   :hide:

   >>> model._meta.update(["X", "Y", "Z"])

Continue from previous example, you can read this back::

   >>> from pyexcel_io import get_data
   >>> data = get_data(DB_DJANGO, models=[model])
   >>> data
   [['X', 'Y', 'Z'], [1, 2, 3], [4, 5, 6]]

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

    >>> to_store = {
    ...    "Sheet1": data['Sheet1'][1:],
    ...    "Sheet2": data['Sheet2'][1:]
    ... }
    >>> models = {
    ...    "Sheet1": [model1, data['Sheet1'][0], None, None],
    ...    "Sheet2": [model2, data['Sheet2'][0], None, None]
    ... }
    >>> save_data(DB_DJANGO, to_store, models=models)
    >>> model1.objects.objs
    [{'Y': 4, 'X': 1, 'Z': 7}, {'Y': 5, 'X': 2, 'Z': 8}, {'Y': 6, 'X': 3, 'Z': 9}]
    >>> model2.objects.objs
    [{'A': 1, 'C': 7, 'B': 4}, {'A': 2, 'C': 8, 'B': 5}, {'A': 3, 'C': 9, 'B': 6}]

.. testcode:
   :hide:

   >>> model1._meta.model_name = "Sheet1"
   >>> model2._meta.model_name = "Sheet2"
   >>> model1._meta.update(["X", "Y", "Z"])
   >>> model2._meta.update(["A", "B", "C"])
   
Read content from multiple tables
--------------------------------------------------------------------------------

Here's what you need to do:

    >>> data = get_data(DB_DJANGO, models=[model1, model2])
    >>> data
    OrderedDict([('Sheet1', [['X', 'Y', 'Z'], [1, 4, 7], [2, 5, 8], [3, 6, 9]]), ('Sheet2', [['A', 'B', 'C'], [1, 4, 7], [2, 5, 8], [3, 6, 9]])])
