from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey

Base = declarative_base()

class Friend(Base):
    __tablename__ = 'indexed_friends'
    id = Column(Integer, primary_key=True)
    user = Column(Integer, ForeignKey('indexed_users.id'), index=True, unique=True)
    index = Column(Integer)
    friend = Column(Integer, ForeignKey('indexed_users.id'))

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, index=True)
    score = Column(Integer)

class IndexedUser(Base):
    __tablename__ = 'indexed_users'
    id = Column(Integer, primary_key=True)
    username = Column(String, index=True, unique=True)
    score = Column(Integer)
