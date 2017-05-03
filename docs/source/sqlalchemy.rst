Working with sqlalchemy
================================================================================

Suppose we have a pure sql database connection via sqlalchemy:

    >>> from sqlalchemy import create_engine
    >>> from sqlalchemy.ext.declarative import declarative_base
    >>> from sqlalchemy import Column , Integer, String, Float, Date
    >>> from sqlalchemy.orm import sessionmaker
    >>> engine=create_engine("sqlite:///sqlalchemy.db")
    >>> Base=declarative_base()
    >>> Session=sessionmaker(bind=engine)


Write data to a database table
--------------------------------------------------------------------------------

Assume we have the following database table::
  
    >>> class Pyexcel(Base):
    ...     __tablename__='pyexcel'
    ...     id=Column(Integer, primary_key=True)
    ...     name=Column(String)
    ...     weight=Column(Float)
    ...     birth=Column(Date)

Let's clear the database and create previous table in the database::

    >>> Base.metadata.create_all(engine)

And suppose we have the following data structure to be saved::

    >>> import datetime
    >>> data = [
    ...     ['birth', 'id', 'name', 'weight'],
    ...     [datetime.date(2014, 11, 11), 0, 'Adam', 11.25],
    ...     [datetime.date(2014, 11, 12), 1, 'Smith', 12.25]
    ... ]

Here's the actual code to achieve it:

    >>> from pyexcel_io import save_data
    >>> from pyexcel_io.constants import DB_SQL, DEFAULT_SHEET_NAME
    >>> from pyexcel_io.database.common import SQLTableImporter, SQLTableImportAdapter
    >>> mysession = Session()
    >>> importer = SQLTableImporter(mysession)
    >>> adapter = SQLTableImportAdapter(Pyexcel)
    >>> adapter.column_names = data[0]
    >>> importer.append(adapter)
    >>> save_data(importer, {adapter.get_name(): data[1:]}, file_type=DB_SQL)

Please note that, the data dict shall have table name as its key. Now let's verify the data:

    >>> from pyexcel_io.database.querysets import QuerysetsReader
    >>> query_sets=mysession.query(Pyexcel).all()
	>>> reader = QuerysetsReader(query_sets, data[0])
    >>> results = reader.to_array()
    >>> import json
    >>> json.dumps(list(results))
    '[["birth", "id", "name", "weight"], ["2014-11-11", 0, "Adam", 11.25], ["2014-11-12", 1, "Smith", 12.25]]'


Read data from a database table
--------------------------------------------------------------------------------

Let's use previous data for reading and see if we could get them via
:meth:`~pyexcel_io.get_data` :

    >>> from pyexcel_io import get_data
    >>> from pyexcel_io.database.common import SQLTableExporter, SQLTableExportAdapter
    >>> exporter = SQLTableExporter(mysession)
    >>> adapter = SQLTableExportAdapter(Pyexcel)
    >>> exporter.append(adapter)
    >>> data = get_data(exporter, file_type=DB_SQL)
    >>> json.dumps(list(data['pyexcel']))
    '[["birth", "id", "name", "weight"], ["2014-11-11", 0, "Adam", 11.25], ["2014-11-12", 1, "Smith", 12.25]]'

Read a subset from the table:
	
    >>> exporter = SQLTableExporter(mysession)
    >>> adapter = SQLTableExportAdapter(Pyexcel, ['birth'])
    >>> exporter.append(adapter)
    >>> data = get_data(exporter, file_type=DB_SQL)
    >>> json.dumps(list(data['pyexcel']))
    '[["birth"], ["2014-11-11"], ["2014-11-12"]]'


Write data to multiple tables
--------------------------------------------------------------------------------

Before we start, let's clear off previous table:

    >>> Base.metadata.drop_all(engine)

Now suppose we have these more complex tables:

    >>> from sqlalchemy import ForeignKey, DateTime
    >>> from sqlalchemy.orm import relationship, backref
    >>> import sys
    >>> class Post(Base):
    ...     __tablename__ = 'post'
    ...     id = Column(Integer, primary_key=True)
    ...     title = Column(String(80))
    ...     body = Column(String(100))
    ...     pub_date = Column(DateTime)
    ... 
    ...     category_id = Column(Integer, ForeignKey('category.id'))
    ...     category = relationship('Category',
    ...         backref=backref('posts', lazy='dynamic'))
    ... 
    ...     def __init__(self, title, body, category, pub_date=None):
    ...         self.title = title
    ...         self.body = body
    ...         if pub_date is None:
    ...             pub_date = datetime.utcnow()
    ...         self.pub_date = pub_date
    ...         self.category = category
    ... 
    ...     def __repr__(self):
    ...         return '<Post %r>' % self.title
    ... 
    >>> class Category(Base):
    ...     __tablename__ = 'category'
    ...     id = Column(Integer, primary_key=True)
    ...     name = Column(String(50))
    ... 
    ...     def __init__(self, name):
    ...         self.name = name
    ... 
    ...     def __repr__(self):
    ...         return '<Category %r>' % self.name
    ...     def __str__(self):
    ...         return self.__repr__()

Let's clear the database and create previous table in the database:

    >>> Base.metadata.create_all(engine)

Suppose we have these data:

    >>> data = {
    ...     "Category":[
    ...         ["id", "name"],
    ...         [1, "News"],
    ...         [2, "Sports"]
    ...     ],
    ...     "Post":[
    ...         ["id", "title", "body", "pub_date", "category"],
    ...         [1, "Title A", "formal", datetime.datetime(2015,1,20,23,28,29), "News"],
    ...         [2, "Title B", "informal", datetime.datetime(2015,1,20,23,28,30), "Sports"]
    ...     ]
    ...  }

Both table has gotten initialization functions:

    >>> def category_init_func(row):
    ...     c = Category(row['name'])
    ...     c.id = row['id']
    ...     return c

and particularly **Post** has a foreign key to **Category**, so we need to
query **Category** out and assign it to **Post** instance

    >>> def post_init_func(row):
    ...     c = mysession.query(Category).filter_by(name=row['category']).first()
    ...     p = Post(row['title'], row['body'], c, row['pub_date'])
    ...     return p

Here's the code to update both:

    >>> tables = {
    ...     "Category": [Category, data['Category'][0], None, category_init_func],
    ...     "Post": [Post, data['Post'][0], None, post_init_func]
    ... }
    >>> from pyexcel_io._compact import OrderedDict
    >>> importer = SQLTableImporter(mysession)
    >>> adapter1 = SQLTableImportAdapter(Category)
    >>> adapter1.column_names = data['Category'][0]
    >>> adapter1.row_initializer = category_init_func
    >>> importer.append(adapter1)
    >>> adapter2 = SQLTableImportAdapter(Post)
    >>> adapter2.column_names = data['Post'][0]
    >>> adapter2.row_initializer = post_init_func
    >>> importer.append(adapter2)
    >>> to_store = OrderedDict()
    >>> to_store.update({adapter1.get_name(): data['Category'][1:]})
    >>> to_store.update({adapter2.get_name(): data['Post'][1:]})
    >>> save_data(importer, to_store, file_type=DB_SQL)

Let's verify what do we have in the database:

    >>> query_sets = mysession.query(Category).all()
    >>> reader = QuerysetsReader(query_sets, data['Category'][0])
	>>> results = reader.to_array()
    >>> import json
    >>> json.dumps(list(results))
    '[["id", "name"], [1, "News"], [2, "Sports"]]'
    >>> query_sets = mysession.query(Post).all()
    >>> reader = QuerysetsReader(query_sets, ["id", "title", "body", "pub_date"])
	>>> results = reader.to_array()
    >>> json.dumps(list(results))
    '[["id", "title", "body", "pub_date"], [1, "Title A", "formal", "2015-01-20T23:28:29"], [2, "Title B", "informal", "2015-01-20T23:28:30"]]'


Skipping existing record
******************************

When you import data into a database that has data already, you can skip existing record if
:class:`pyexcel_io.PyexcelSQLSkipRowException` is raised. Example can be found here in `test 
code <https://github.com/chfw/pyexcel-io/blob/master/tests/test_sql_book.py#L125>`_.

Update existing record
***************************

When you import data into a database that has data already, you can update an existing record
if you can query it from the database and set the data yourself and most importantly return it.
You can find an example in `test skipping row  <https://github.com/chfw/pyexcel-io/blob/master/tests/test_sql_book.py#L162>`_

Read data from multiple tables
----------------------------------------------------------------------------------

Let's use previous data for reading and see if we could get them via
:meth:`~pyexcel_io.get_data` :

    >>> exporter = SQLTableExporter(mysession)
    >>> adapter = SQLTableExportAdapter(Category)
    >>> exporter.append(adapter)
    >>> adapter = SQLTableExportAdapter(Post)
    >>> exporter.append(adapter)
    >>> data = get_data(exporter, file_type=DB_SQL)
    >>> json.dumps(data)
    '{"category": [["id", "name"], [1, "News"], [2, "Sports"]], "post": [["body", "category_id", "id", "pub_date", "title"], ["formal", 1, 1, "2015-01-20T23:28:29", "Title A"], ["informal", 2, 2, "2015-01-20T23:28:30", "Title B"]]}'

What if we read a subset per each table

    >>> exporter = SQLTableExporter(mysession)
    >>> adapter = SQLTableExportAdapter(Category, ['name'])
    >>> exporter.append(adapter)
    >>> adapter = SQLTableExportAdapter(Post, ['title'])
    >>> exporter.append(adapter)
    >>> data = get_data(exporter, file_type=DB_SQL)
    >>> json.dumps(data)
    '{"category": [["name"], ["News"], ["Sports"]], "post": [["title"], ["Title A"], ["Title B"]]}'

.. testcode::
   :hide:

   >>> mysession.close()
   >>> import os
   >>> os.unlink('sqlalchemy.db')
