from sqlalchemy import create_engine, Column, String, Text, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool

engine = create_engine('sqlite:///allo_scrapper.db', echo=False, poolclass=QueuePool)
_SessionFactory = sessionmaker(bind=engine)

Base = declarative_base()


def session_factory():
    Base.metadata.create_all(engine)
    return _SessionFactory()

class AlloTips(Base):
    __tablename__ = 'allo_tips'
    id = Column(Integer, primary_key=True, autoincrement=True)
    request = Column(String(3), unique=True)
    queries = relationship("Query", secondary='link')
    products = relationship("Product", secondary='link')
    categories = relationship("Category", secondary='link')
    processed = Column(Boolean, default=False)

class Query(Base):
    __tablename__ = "queries"
    id = Column(Integer, primary_key=True, autoincrement=True)
    query = Column(String, unique=True)
    tips = relationship("AlloTips", secondary='link')

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    url = Column(String)
    price = Column(String)
    image = Column(String)
    special_price = Column(String)
    tips = relationship("AlloTips", secondary='link')

class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True)
    tips = relationship("AlloTips", secondary='link')

class Link(Base):
    __tablename__ = 'link'
    id = Column(Integer, primary_key=True, autoincrement=True)
    tip_id = Column(String, ForeignKey('allo_tips.id'))
    query_id = Column(Integer, ForeignKey('queries.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    category_id = Column(Integer, ForeignKey('categories.id'))

sess = session_factory()

def get_or_create(model, parameters):
    """
    Get or create a model instance while preserving integrity.
    """
    exist = sess.query(model).filter_by(**parameters).first()
    if exist:
        return exist
    else:
        return model(**parameters)


