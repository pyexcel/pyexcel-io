from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column , Integer, String, Float, Date, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker
import datetime
from pyexcel_io import (
    DB_SQL,
    get_data,
    save_data,
    from_query_sets,
    DEFAULT_SHEET_NAME
)
from sqlalchemy.orm import relationship, backref

engine=create_engine("sqlite:///tmp.db")
Base=declarative_base()

class Pyexcel(Base):
    __tablename__='pyexcel'
    id=Column(Integer, primary_key=True)
    name=Column(String)
    weight=Column(Float)
    birth=Column(Date)

class Post(Base):
    __tablename__ = 'post'
    id = Column(Integer, primary_key=True)
    title = Column(String(80))
    body = Column(String(100))
    pub_date = Column(DateTime)

    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship('Category',
        backref=backref('posts', lazy='dynamic'))

    def __init__(self, title, body, category, pub_date=None):
        self.title = title
        self.body = body
        if pub_date is None:
            pub_date = datetime.utcnow()
        self.pub_date = pub_date
        self.category = category

    def __repr__(self):
        return '<Post %r>' % self.title

class Category(Base):
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Category %r>' % self.name
    def __str__(self):
        return self.__repr__()
    
Session=sessionmaker(bind=engine)

class TestSingleRead:
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
            
        
class TestSingleWrite:
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
                  tables={ DEFAULT_SHEET_NAME: [Pyexcel,self.data[0], None, None]}
              )
        query_sets=mysession.query(Pyexcel).all()
        results = from_query_sets(self.data[0], query_sets)
        assert results == self.results



class TestMultipleRead:
    def setUp(self):
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)
        self.session = Session()
        data = {
            "Category":[
                ["id", "name"],
                [1, "News"],
                [2, "Sports"]
            ],
            "Post":[
                ["id", "title", "body", "pub_date", "category"],
                [1, "Title A", "formal", datetime.datetime(2015,1,20,23,28,29), "News"],
                [2, "Title B", "informal", datetime.datetime(2015,1,20,23,28,30), "Sports"]
            ]
         }
        def category_init_func(row):
            c = Category(row['name'])
            c.id = row['id']
            return c
        
        def post_init_func(row):
            c = self.session.query(Category).filter_by(name=row['category']).first()
            p = Post(row['title'], row['body'], c, row['pub_date'])
            return p
        tables = {
            "Category": [Category, data['Category'][0], None, category_init_func],
            "Post": [Post, data['Post'][0], None, post_init_func]
        }
        to_store = {
           "Category": data['Category'][1:],
           "Post": data['Post'][1:]
        }
        save_data(DB_SQL, to_store, session=self.session, tables=tables)

    def test_read(self):
        data = get_data(DB_SQL, session=self.session, tables=[Category, Post])
        import json
        assert json.dumps(data) == '{"category": [["id", "name"], [1, "News"], [2, "Sports"]], "post": [["body", "category_id", "id", "pub_date", "title"], ["formal", 1, 1, "2015-01-20T23:28:29", "Title A"], ["informal", 2, 2, "2015-01-20T23:28:30", "Title B"]]}'

    def tearDown(self):
        self.session.close()