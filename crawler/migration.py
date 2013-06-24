import time

import db
from schema import User
import sqlalchemy

count = 0
session = db.get_session()
start = time.time()
PAGE_SIZE = 1000
while True:
    users = session.query(User).order_by(User.id).limit(PAGE_SIZE).offset(count * PAGE_SIZE)
    for user in users:
        try:
            db.add_indexed_user(session, user)
        except sqlalchemy.exc.IntegrityError:
            session.rollback()
            with open('duplicates.csv', 'a') as f:
                f.write('{},{}\n'.format(user.username, user.id))
    count += 1
    print "{} users crawled, {} seconds elapsed".format(count * PAGE_SIZE, int(time.time() - start))
