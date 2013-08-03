from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from . import schema

ENGINE = create_engine('postgresql://kevin:@localhost:5432')
Session = sessionmaker(bind=ENGINE)
session = Session()
session.query(schema.Friend).filter_by(friend=593).all()
