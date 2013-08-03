import time
import sys

from sqlalchemy import and_

from schema import User
import db
# For all users:
session = db.get_session()
count = 0
start = time.time()

while True:
    users = session.query(User).order_by(User.id).limit(1000).offset(count * 1000)
    # Find a matching user with a higher auto id in the database.
    for user in users:
        other_users = session.query(User).filter(and_(
            User.username==user.username, User.id>user.id)).all()
        if len(other_users) == 0:
            sys.stdout.write('.')
            sys.stdout.flush()
            continue

        last_user = other_users[-1]
        print "\nFound another user for {}, lower id is {}, newer is {}".format(
            user.username, user.id, last_user.id)

        # Update all of the older users' references in the friends database to point to
        # the new user.
        for friend in db.find_friends(session, user):
            friend.friend = last_user.id
            print "Friend {} in friends has new base user {}".format(
                friend.friend, last_user.id)
            session.commit()

        # delete all references to the older user. the newer user should be the
        # source of truth
        for friend in db.find_user_in_friends(session, user):
            print "Deleted friend {}".format(friend.user)
            session.delete(friend)
            session.commit()
        print "Deleted duplicate user {}".format(user.username)
        session.delete(user)
        session.commit()
    count += 1
    print count * 1000
    print time.time() - start


# Delete the old users friend records
# Delete the user
