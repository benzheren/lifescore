from celery.task import task
from celery.loaders.default import Loader
from sqlalchemy import create_engine

from lifescore.models import DBSession, Base, Friend

loader = Loader()
engine = create_engine(loader.read_configuration()['CELERY_RESULT_DBURI'])
dbsession = DBSession()
dbsession.configure(bind=engine)
Base.metadata.bind = engine

@task
def save_friends(friends, scores, user):
    for i in range(len(friends)):
        friend = Friend(friends[i]['id'], friends[i]['name'], 
                        'gender' in friends[i] and friends[i]['gender'] or None, 
                        'location' in friends[i] and 
                        friends[i]['location']['name'] or None, 
                        scores[i]['score'])
        friend.user_id = user.id
        dbsession.add(friend)

    dbsession.commit()
