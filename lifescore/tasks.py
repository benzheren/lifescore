from celery.task import task
from sqlalchemy import create_engine

from lifescore.models import DBSession, Base, Friend

engine = create_engine('mysql+mysqldb://lifescore:5mad_cows@localhost/lifescore?charset=utf8&use_unicode=0')
dbsession = DBSession()
dbsession.configure(bind=engine)
Base.metadata.bind = engine

@task
def save_friends(friends, scores, user):
    for i in range(len(friends)):
        friend = Friend(friends[i]['id'], 'gender' in friends[i] and
                        friends[i]['gender'] or None, 'location' in friends[i]
                        and friends[i]['location']['name'] or None, scores[i]['score'])
        friend.user_id = user.id
        dbsession.add(friend)

    dbsession.commit()

@task
def add(x, y):
    return x + y
