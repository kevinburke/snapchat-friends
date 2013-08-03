import time
import sys

from sqlalchemy import and_

from schema import Friend
import db
# For all users:
session = db.get_session()
try:
    start = count = int(sys.argv[1])
except:
    start = count = 0

start = time.time()

def get_friends(session, friend):
    return session.query(Friend).filter(and_(
        Friend.id       >    friend.id,
        Friend.user     ==   friend.user,
        Friend.friend   ==   friend.friend,
        Friend.index    ==   friend.index
    ))

while count - 1000*1000 < start:
    friends = session.query(Friend).filter(Friend.id>count).order_by(Friend.id).limit(1000)
    for friend in friends:
        others = get_friends(session, friend)
        dupes = 0
        for other in others:
            session.delete(other)
            try:
                session.commit()
            except:
                # assume someone else got there
                pass
            dupes += 1
        if dupes:
            print "\nDeleted {} dupes of user {} with index {} and friend {}".format(
                dupes, friend.user, friend.index, friend.friend)

    if count % 100000 == 0:
        print count
        print str(int(time.time() - start)) + " seconds"
    count += 1000
print "done"
