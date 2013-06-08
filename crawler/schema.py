from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey

Base = declarative_base()

class Friend(Base):
    __tablename__ = 'friends'
    id = Column(Integer, primary_key=True)
    user = Column(Integer, ForeignKey('users.id'))
    index = Column(Integer)
    friend = Column(Integer, ForeignKey('users.id'))

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, index=True)
    score = Column(Integer)
