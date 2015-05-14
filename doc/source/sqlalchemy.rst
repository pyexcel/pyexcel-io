Working with sqlalchemy
================================================================================

Suppose we have a pure sql database connection via sqlalchemy:

    >>> from sqlalchemy import create_engine
    >>> from sqlalchemy.ext.declarative import declarative_base
    >>> from sqlalchemy import Column , Integer, String, Float, Date
    >>> from sqlalchemy.orm import sessionmaker
    >>> engine=create_engine("sqlite:///tmp.db")
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

Let's clear the database and create previous table in the database:

    >>> Base.metadata.drop_all(engine)
    >>> Base.metadata.create_all(engine)

And suppose we have the following data structure to be saved:

    >>> import datetime
    >>> data = [
    ...     ['birth', 'id', 'name', 'weight'],
    ...     [datetime.date(2014, 11, 11), 0, 'Adam', 11.25],
    ...     [datetime.date(2014, 11, 12), 1, 'Smith', 12.25]
    ... ]

Here's the actual code to achieve it:

    >>> from pyexcel_io import save_data, DB_SQL, DEFAULT_SHEET_NAME
    >>> mysession = Session()
    >>> save_data(DB_SQL,
    ...      data[1:],
    ...      session=mysession,
    ...      tables={ DEFAULT_SHEET_NAME: [Pyexcel, data[0], None, None] }
    ... )

Now let's verify the data:

    >>> from pyexcel_io import from_query_sets
    >>> query_sets=mysession.query(Pyexcel).all()
    >>> results = from_query_sets(data[0], query_sets)
    >>> import json
    >>> json.dumps(results)
    '[["birth", "id", "name", "weight"], ["2014-11-11", 0, "Adam", 11.25], ["2014-11-12", 1, "Smith", 12.25]]'


Read data from a database table
--------------------------------------------------------------------------------

Let's use previous data for reading and see if we could get them via
:meth:`~pyexcel_io.get_data` :

    >>> from pyexcel_io import get_data
    >>> data = get_data(DB_SQL, session=mysession, tables=[Pyexcel])
    >>> json.dumps(results)
    '[["birth", "id", "name", "weight"], ["2014-11-11", 0, "Adam", 11.25], ["2014-11-12", 1, "Smith", 12.25]]'


Write data to multiple tables
--------------------------------------------------------------------------------

Before we start, let's clear off previous table:

    >>> Base.metadata.drop_all(engine)

Now suppose we have these more complex tables:

    >>> from sqlalchemy import ForeignKey, DateTime
    >>> from sqlalchemy.orm import relationship, backref
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
	>>> to_store = {
	...    "Category": data['Category'][1:],
	...    "Post": data['Post'][1:]
	... }
    >>> save_data(DB_SQL, to_store, session=mysession, tables=tables)

Let's verify what do we have in the database:

    >>> query_sets = mysession.query(Category).all()
    >>> results = from_query_sets(data['Category'][0], query_sets)
    >>> import json
    >>> json.dumps(results)
    '[["id", "name"], [1, "News"], [2, "Sports"]]'
    >>> query_sets = mysession.query(Post).all()
    >>> results = from_query_sets(["id", "title", "body", "pub_date"], query_sets)
    >>> json.dumps(results)
    '[["id", "title", "body", "pub_date"], [1, "Title A", "formal", "2015-01-20T23:28:29"], [2, "Title B", "informal", "2015-01-20T23:28:30"]]'


Read data from multiple tables
----------------------------------------------------------------------------------

Let's use previous data for reading and see if we could get them via
:meth:`~pyexcel_io.get_data` :

    >>> data = get_data(DB_SQL, session=mysession, tables=[Category, Post])
    >>> json.dumps(data)
    '{"category": [["id", "name"], [1, "News"], [2, "Sports"]], "post": [["body", "category_id", "id", "pub_date", "title"], ["formal", 1, 1, "2015-01-20T23:28:29", "Title A"], ["informal", 2, 2, "2015-01-20T23:28:30", "Title B"]]}'

.. testcode::
   :hide:

   >>> mysession.close()
   >>> import os
   >>> os.unlink('tmp.db')
