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
def test_migrate():
    session = db.get_session(SESSION)

