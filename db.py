import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from schema import Friend, User

def _get_filename_dir():
    return os.path.join(os.path.dirname(__file__))

ENGINE = create_engine('sqlite:///{}/snapchat.db'.format(_get_filename_dir()))

Session = sessionmaker(bind=ENGINE)

def create_user(name, score=-1):
    user = User(username=name, score=score)
    session = Session()
    session.add(user)
    session.commit()
    return user.id

def add(user_id, friend_id, index):
    friend = Friend(user=user_id, friend=friend_id, index=index)
    session = Session()
    session.add(friend)
    session.commit()

def exists(username):
    session = Session()
    return session.query(User).filter_by(username=username).first()
