from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column , Integer, String, Float, Date
from sqlalchemy.orm import sessionmaker
import datetime
from pyexcel_io import DB_SQL, get_data, save_data, from_query_sets

engine=create_engine("sqlite:///tmp.db")
Base=declarative_base()

class Pyexcel(Base):
    __tablename__='pyexcel'
    id=Column(Integer, primary_key=True)
    name=Column(String)
    weight=Column(Float)
    birth=Column(Date)

class Signature(Base):
    __tablename__="signature"
    X=Column(Integer, primary_key=True)
    Y=Column(Integer)
    Z=Column(Integer)

class Signature2(Base):
    __tablename__="signature2"
    A=Column(Integer, primary_key=True)
    B=Column(Integer)
    C=Column(Integer)
    
Session=sessionmaker(bind=engine)

class TestSQL:
    def setUp(self):
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)
        p1 = Pyexcel(id=0,
                     name="Adam",
                     weight=11.25,
                     birth=datetime.date(2014, 11, 11))
        self.session = Session()
        self.session.add(p1)
        p1 = Pyexcel(id=1,
                     name="Smith",
                     weight=12.25,
                     birth=datetime.date(2014, 11, 12))
        self.session.add(p1)
        self.session.commit()
        self.session.close()

    def test_sql(self):
        mysession=Session()
        data = get_data(DB_SQL, session=mysession, tables=[Pyexcel])
        content = [
            ['birth', 'id', 'name', 'weight'],
            ['2014-11-11', 0, 'Adam', 11.25],
            ['2014-11-12', 1, 'Smith', 12.25]
        ]
        assert data == content
        mysession.close()
            
        
class TestWritingSQL:
    def setUp(self):
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)
        self.data = [
            ['birth', 'id', 'name', 'weight'],
            [datetime.date(2014, 11, 11), 0, 'Adam', 11.25],
            [datetime.date(2014, 11, 12), 1, 'Smith', 12.25]
        ]
        self.results = [
            ['birth', 'id', 'name', 'weight'],
            ['2014-11-11', 0, 'Adam', 11.25],
            ['2014-11-12', 1, 'Smith', 12.25]
        ]

    def test_one_table(self):
        mysession = Session()
        save_data(DB_SQL,
                  self.data[1:],
                  session=mysession,
                  tables={ 'csv': [Pyexcel,self.data[0], None, None]}
              )
        query_sets=mysession.query(Pyexcel).all()
        results = from_query_sets(self.data[0], query_sets)
        assert results == self.results
