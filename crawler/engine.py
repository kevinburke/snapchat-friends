from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import schema

ENGINE = create_engine('postgresql://kevin:@localhost:5432/', echo=True)
Session = sessionmaker(bind=ENGINE)
session = Session()
import time
now = time.time()
friends = session.query(schema.Friend).filter_by(user=593).all()
print time.time() - now

for friend in friends:
    print friend.user
print time.time() - now
