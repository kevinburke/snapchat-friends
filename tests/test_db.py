from nose.tools import assert_equal

import db

def test_duplicates():
    session = db.get_session()
    user_id = db.create_user(session, 'kevin')
    second_user_id = db.create_user(session, 'kevin')

    assert_equal(user_id, second_user_id)

def test_add_score():
    session = db.get_session()
    db.create_user(session, 'kevin')
    db.create_user(session, 'kevin', 22)

    session = db.get_session()
    user = db.exists(session, 'kevin')
    assert_equal(22, user.score)
