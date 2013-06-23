import db
from schema import User
import sqlalchemy

count = 0
session = db.get_session()
while True:
    users = session.query(User).order_by(User.id).limit(10).offset(count * 1000)
    for user in users:
        try:
            db.add_indexed_user(session, user)
        except sqlalchemy.exc.IntegrityError:
            session.rollback()
            with open('duplicates.csv', 'a') as f:
                f.write('{},{}\n'.format(user.username, user.id))
    count += 1
    print "{} users crawled".format(count * 1000)
