Working with sqlalchemy
================================================================================

Suppose we have a pure sql database connection via sqlalchemy:

    >>> from sqlalchemy import create_engine
    >>> from sqlalchemy.ext.declarative import declarative_base
    >>> from sqlalchemy import Column , Integer, String, Float, Date, ForeignKey, backref, DateTime
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

    >>> from pyexcel_io import save_data, DB_SQL
    >>> mysession = Session()
    >>> save_data(DB_SQL,
    ...      data[1:],
    ...      session=mysession,
    ...      tables={ 'csv': [Pyexcel, data[0], None, None]}
    ... )

Now let's verify the data:

    >>> from pyexcel_io import from_query_sets
    >>> query_sets=mysession.query(Pyexcel).all()
    >>> results = from_query_sets(data[0], query_sets)
    >>> import pprint
    >>> pprint.pprint(results)
    [['birth', 'id', 'name', 'weight'],
     ['2014-11-11', 0, u'Adam', 11.25],
     ['2014-11-12', 1, u'Smith', 12.25]]


Read data from a database table
--------------------------------------------------------------------------------

Let's use previous data for reading and see if we could get them via
:meth:`~pyexcel_io.get_data` :

    >>> from pyexcel_io import get_data
    >>> data = get_data(DB_SQL, session=mysession, tables=[Pyexcel])
    >>> pprint.pprint(data)
    [['birth', 'id', 'name', 'weight'],
     ['2014-11-11', 0, u'Adam', 11.25],
     ['2014-11-12', 1, u'Smith', 12.25]]


Write data to multiple tables
--------------------------------------------------------------------------------

Suppose we have these more complex tables:

    >>> class Post(Base):
    ...     __tablename__ = 'Post'
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
    ...     __tablename__ = 'Category'
    ...     id = Column(Integer, primary_key=True)
    ...     name = Column(String(50))
    ... 
    ...     def __init__(self, name):
    ...         self.name = name
    ... 
    ...     def __repr__(self):
    ...         return '<Category %r>' % self.name

Let's clear the database and create previous table in the database:

    >>> Base.metadata.drop_all(engine)
    >>> Base.metadata.create_all(engine)

Suppose we have these data:

    ... data = {
    ...     "Category":[
    ...         ["id", "name"],
    ...         [1, "News"],
    ...         [2, "Sports"]
    ...     ],
    ...     "Post":[
    ...         ["id", "title", "body", "pub_date", "category"],
    ...         [1, "Title A", "formal", datetime(2015,1,20,23,28,29), "News"],
    ...         [2, "Title B", "informal", datetime(2015,1,20,23,28,30), "Sports"]
    ...     ]
    ... }

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
    >>> save_data(DB_SQL, data, session=mysession, tables=tables)
