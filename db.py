import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from schema import Friend, User

def _get_filename_dir():
    return os.path.join(os.path.dirname(__file__))

ENGINE = create_engine('sqlite:///{}/snapchat.db'.format(_get_filename_dir()))

Session = sessionmaker(bind=ENGINE)

def create_user(name, score=-1):
    session = Session()
    user = exists(name)
    if user:
        user.score = score
    else:
        user = User(username=name, score=score)
        session.add(user)
    session.commit()
    return user.id

def add(user_id, friend_id, index):
    friend = Friend(user=user_id, friend=friend_id, index=index)
    session = Session()
    session.add(friend)
    session.commit()

def find_queued_users():
    session = Session()
    return session.query(User).filter_by(score=-1).with_entities(User.username)

def exists(username):
    session = Session()
    return session.query(User).filter_by(username=username).first()
