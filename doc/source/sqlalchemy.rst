Working with sqlalchemy
================================================================================

Suppose we have a pure sql database connection via sqlalchemy:

    >>> from sqlalchemy import create_engine
    >>> from sqlalchemy.ext.declarative import declarative_base
    >>> from sqlalchemy import Column , Integer, String, Float, Date, ForeignKey, DateTime
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


