import time

import db
from schema import Friend
import sqlalchemy

count = 0
session = db.get_session()
start = time.time()
PAGE_SIZE = 1000
while True:
    friends = session.query(Friend).order_by(Friend.id).limit(10).offset(count * PAGE_SIZE)
    for friend in friends:
        try:
            db.add_indexed_friend(session, friend)
        except sqlalchemy.exc.IntegrityError:
            session.rollback()
            with open('duplicates.csv', 'a') as f:
                f.write('{},{}\n'.format(friend.user, friend.id, friend.friend))
    count += 1
    print "{} friends crawled, {} seconds elapsed".format(count * PAGE_SIZE, int(time.time() - start))

