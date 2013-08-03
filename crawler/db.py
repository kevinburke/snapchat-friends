import ConfigParser
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from schema import Friend, User, IndexedUser, IndexedFriend

def _get_filename_dir():
    return os.path.join(os.path.dirname(__file__))


#if 'darwin' in sys.platform.lower():
    #ENGINE = create_engine('sqlite:///{}/snapchat.db'.format(_get_filename_dir()))
#else:
config = ConfigParser.RawConfigParser()
config.read('app.cfg')
ENGINE = create_engine('postgresql://{user}:{password}'
                       '@{host}:{port}/{database}'.format(
                           user=config.get('default', 'username'),
                           password=config.get('default', 'password'),
                           port=config.get('default', 'port'),
                           host=config.get('default', 'host'),
                           database=config.get('default', 'database'),
                       #), echo=True)
                       ))
print ENGINE
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

def add_indexed_user(session, user):
    iuser = IndexedUser(username=user.username, score=user.score)
    session.add(iuser)
    session.commit()

def add_indexed_friend(session, friend):
    iuser = IndexedFriend(user=friend.user, index=friend.index, friend=friend.friend)
    session.add(iuser)
    session.commit()

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


def find_friends(session, user):
    return session.query(Friend).filter_by(friend=user.id)


def find_user_in_friends(session, user):
    return session.query(Friend).filter_by(user=user.id)
