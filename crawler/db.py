import ConfigParser
import os
import sys

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from schema import Friend, User

def _get_filename_dir():
    return os.path.join(os.path.dirname(__file__))


if 'darwin' in sys.platform.lower():
    ENGINE = create_engine('sqlite:///{}/snapchat.db'.format(_get_filename_dir()))
else:
    config = ConfigParser.RawConfigParser()
    config.read('app.cfg')
    ENGINE = create_engine('postgresql://{user}:{password}'
                           '@localhost:{port}/snapchat'.format(
                               user=config.get('default', 'username'),
                               password=config.get('default', 'password'),
                               port=config.get('default', 'port'),
                           ))
Session = sessionmaker(bind=ENGINE)

def get_session(session=Session):
    return session()


def create_user(session, name, score=-1):
    user = exists(session, name)
    if user:
        user.score = score
    else:
        user = User(username=name, score=score)
        session.add(user)
    session.commit()
    return user

def add(session, user_id, friend_id, index):
    friend = Friend(user=user_id, friend=friend_id, index=index)
    session.add(friend)
    session.commit()


def find_queued_users(session, limit=200):
    return session.query(User).filter_by(score=-1)\
            .with_entities(User.username).limit(limit)


def get_count(session=None):
    if not session:
        session = Session()
    return session.query(User).count()


def exists(session, username):
    return session.query(User).filter_by(username=username).first()
