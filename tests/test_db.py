from nose.tools import assert_equal, with_setup
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import db
from db import Friend, User

SESSION = None

def setup_func():
    global SESSION
    engine = create_engine('sqlite:///')
    Friend.metadata.create_all(engine)
    User.metadata.create_all(engine)
    SESSION = sessionmaker(bind=engine)

@with_setup(setup_func)
def test_duplicates():
    session = db.get_session(SESSION)
    user_id = db.create_user(session, 'kevin')
    second_user_id = db.create_user(session, 'kevin')

    assert_equal(user_id, second_user_id)

@with_setup(setup_func)
def test_add_score():
    session = db.get_session(SESSION)
    db.create_user(session, 'kevin')
    db.create_user(session, 'kevin', 22)

    session = db.get_session()
    user = db.exists(session, 'kevin')
    assert_equal(22, user.score)

@with_setup(setup_func)
def test_count():
    session = db.get_session(SESSION)
    assert_equal(0, db.get_count(session))
    db.create_user(session, 'kevin')
    assert_equal(1, db.get_count(session))

