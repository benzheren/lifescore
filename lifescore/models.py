import transaction

from sqlalchemy import Column, Integer, String, TIMESTAMP, Unicode
from sqlalchemy import func

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

DBSession = scoped_session(sessionmaker())
Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    fb_id = Column(String(255), unique=True)
    fb_access_token = Column(String(255))
    fb_updated_time = Column(TIMESTAMP)
    score = Column(Integer)
    created = Column(TIMESTAMP, default=func.current_timestamp())

    def __init__(self, fb_id=None, fb_access_token=None, fb_updated_time=None,
                 score=0):
        self.fb_id = fb_id
        self.fb_access_token = fb_access_token
        self.fb_updated_time = fb_updated_time
        self.score = score


class NationalSchools(Base):
    __tablename__ = 'national_schools'

    id = Column(Integer, primary_key=True)
    rank = Column(Integer)
    name = Column(Unicode(255))
    city = Column(Unicode(255))
    short_name = Column(Unicode(255))

class WorldSchools(Base):
    __tablename__ = 'world_schools'

    id = Column(Integer, primary_key=True)
    rank = Column(Integer)
    name = Column(Unicode(255))
    city = Column(Unicode(255))
    short_name = Column(Unicode(255))

def initialize_sql(engine):
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    Base.metadata.create_all(engine)
    #try:
    #    populate()
    #except IntegrityError:
    #    DBSession.rollback()
