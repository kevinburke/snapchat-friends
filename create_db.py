import db
from db import ENGINE, Friend, User

Friend.metadata.create_all(ENGINE)
User.metadata.create_all(ENGINE)
