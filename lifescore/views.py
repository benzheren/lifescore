import random

from beaker.cache import cache_region
import facebook
import memcache
from pyramid.view import view_config
from pyramid.url import route_url
from sqlalchemy.sql.expression import desc

from lifescore import tasks
from lifescore.models import User, NationalSchools, WorldSchools, Company
from lifescore.models import Friend
from lifescore.models import DBSession


RELATIONSHIPS = {'Single': 1, 'In a relationship': 1.1, 'Engaged': 1.2, 
                     'Married': 1.3, 'It\'s complicated': 0.9, 
                     'In an open relationship': 0.9, 'Windowed': 1,
                     'Separated': 0.8, 'Divorced': 0.7, 
                     'In a civil union': 1.3, 'In a domestic partnership': 1.3}

@view_config(route_name='home', renderer='home.mak')
def home(request):
    dbsession = DBSession()
    settings = request.registry.settings
    fb_perms = ['user_education_history', 'friends_education_history',
                'publish_stream', 'offline_access',
                'user_relationships', 'friends_relationships',
                'user_work_history', 'friends_work_history',
                'user_location', 'friends_location']

    cookie = facebook.get_user_from_cookie(request.cookies,
                                           settings['facebook.app.id'],
                                           settings['facebook.app.secret'])

    if cookie:
        graph = facebook.GraphAPI(cookie['access_token'])
        profile = graph.get_object('me')
        dashboard_url = route_url('dashboard', request, fb_id=profile['id'])
        request.response_cookies = request.cookies
        return dict(dashboard_url=dashboard_url, 
                    facebook_app_id=settings['facebook.app.id'])
    else:
        return dict(facebook_app_id=settings['facebook.app.id'], 
                    facebook_perms=','.join(fb_perms))

@view_config(route_name='dashboard', renderer='dashboard.mak')
def dashboard(request):
    dbsession = DBSession()
    settings = request.registry.settings
    cookie = facebook.get_user_from_cookie(request.cookies,
                                           settings['facebook.app.id'],
                                           settings['facebook.app.secret'])
    if cookie:
        graph = _get_graph(cookie['access_token'])
        profile = graph.get_object('me')
        fb_id = profile['id']
        user = dbsession.query(User).filter(User.fb_id==fb_id).first()
        if not user:
            user = User(fb_id, cookie['access_token'], profile['updated_time'], 
                       profile['name'], 'gender' in profile and
                        profile['gender'] or None, 'location' in profile and
                        profile['location']['name'] or None, 
                        _get_lifescore(profile))
            dbsession.add(user)
            dbsession.commit()
            return dict(profile=profile,
                        friends_id=_get_friends_id(graph).encode('ascii', 'ignore'))
        elif user.fb_access_token != cookie['access_token']:
            user.fb_access_token = cookie['access_token']
            if user.fb_updated_time != profile['update_time']:
                user.score = _get_lifescore(profile)
            dbsession.merge(user)
            dbsession.commit()

        return dict(profile=profile,
                        friends_id=_get_friends_id(graph).encode('ascii', 'ignore'))
            #fecth existing data from db and return the dashboard
    else:
        # need redirect to a 404 error page
        fb_id = 'no cookie'
        pass
    
    return dict(fb_id=fb_id)

@view_config(route_name='fetch_friends', renderer='json')
def fetch_friends(request):
    friends_id = request.GET['friends_id']
    user = _get_user_from_fb_id(request.GET['fb_id'])
    graph = _get_graph(user.fb_access_token)
    friends = graph.get_objects(friends_id.split(','))
    scores = [dict(id=f['id'], name=f['name'], score=_get_lifescore(f)) 
              for f in friends.itervalues()]
    tasks.save_friends.delay(friends.values(), scores, user)
    try:
        top_friends = request.session['top_friends']
        top_friends.extend(scores)
        top_friends = sorted(top_friends, key=lambda k: k['score'], 
                             reverse=True)[0:20]
        request.session['top_friends'] = top_friends
        return top_friends
    except KeyError:
        request.session['top_friends'] = scores
        return scores

@view_config(route_name='friends_rank_fetch', renderer='json')
def friends_rank_fetch(request):
    try:
        friends_rank = request.session['friends_rank']
    except KeyError:
        user = _get_user_from_fb_id(request.GET['fb_id'])
        friends_rank = _get_friends(user)
        request.session['friends_rank'] = friends_rank
        start = request.GET.get('start', 0)
        return friends_rank[start:(start + 20)]

@view_config(route_name='world_rank_fetch', renderer='json')
def world_rank_fetch(request):
    start = request.GET.get('start', 0)
    return _get_world_rank()[start:(start + 20)]

@cache_region('short_term', 'graph')
def _get_graph(access_token):
    return facebook.GraphAPI(access_token)

@cache_region('short_term', 'user_in_db')
def _get_user_from_fb_id(fb_id):
    dbsession = DBSession()
    return dbsession.query(User).filter(User.fb_id==fb_id).first()

@cache_region('short_term', 'friends_in_db')
def _get_friends(user):
    dbsession = DBSession()
    return dbsession.query(Friend).filter(Friend.user_id==user.id).\
            order_by(desc(Friend.score)).all()

@cache_region('short_term', 'world_rank')
def _get_world_rank():
    dbsession = DBSession()
    world_top = dbsession.query(Friend).order_by(desc(Friend.score)).\
            limit(100).all()
    world_top_users = dbsession.query(User).order_by(desc(User.score)).\
            limit(100).all()
    world_top.extend(world_top_users)
    return sorted(world_top, key=lambda k:k.score, reverse=True)

def _get_friends_id(graph):
    return ','.join([f['id'] for f in graph.get_connections('me',
                                                            'friends')['data']])

def _get_lifescore_influenced(graph):
    score = _get_lifescore(graph.get_object('me'))
    friends = graph.get_connections('me', 'friends')['data']
    for f in friends:
        score += _get_lifescore(graph.get_object(f['id']))
    return score

def _get_lifescore(profile):
    score = (_get_education_score(profile) + _get_work_score(profile)) * \
            _get_relationship_score(profile) * _get_family_score(profile)
    #location = profile['location']
    #gender = profile['gender']
    return random.randint(400, 850)

def _get_education_score(profile):
    try:
        schools = profile['education']
        score = 0
        for s in schools:
            if s['type'] == 'College':
                score += _get_school_rank(s['school']['name'])
            elif s['type'] == 'Graduate School':
                score += 1.5 * _get_school_rank(s['school']['name'])
        return score
    except KeyError:
        return 0

@cache_region('long_term', 'major_rank')
def _get_major_rank(major):
    return 0

@cache_region('long_term', 'single_school_rank')
def _get_school_rank(name):
    try:
        national_rank = _get_all_national_schools()['names'].index(name)
    except ValueError:
        try:
            national_rank = _get_all_national_schools()['short_names'].index(name)
        except ValueError:
            national_rank = 500
    try:
        world_rank = _get_all_world_schools()['names'].index(name)
    except ValueError:
        try:
            world_rank = _get_all_world_schools()['short_names'].index(name)
        except ValueError:
            world_rank = 500

    if national_rank < world_rank:
        return 500 - national_rank
    else:
        return 500 - world_rank

@cache_region('long_term', 'world_schools')
def _get_all_world_schools():
    dbsession = DBSession()
    schools = dbsession.query(WorldSchools.rank, WorldSchools.name,
                    WorldSchools.short_name).all()
    names = [s.name for s in schools]
    short_names = [s.short_name for s in schools]
    return dict(names=names, short_names=short_names)

@cache_region('long_term', 'national_schools')
def _get_all_national_schools():
    dbsession = DBSession()
    schools = dbsession.query(NationalSchools.rank, NationalSchools.name,
                    NationalSchools.short_name).all()
    names = [s.name for s in schools]
    short_names = [s.short_name for s in schools]
    return dict(names=names, short_names=short_names)

def _get_work_score(profile):
    try:
        employers = profile['work']
        score = 0
        for e in employers:
            score += _get_employer_score(e['employer']['name']) * \
                    _get_job_prestige(e)
        return score
    except KeyError:
        return 0

def _get_job_prestige(work):
    try:
        position = work['position']['name']
        return 1
    except KeyError:
        return 1

@cache_region('long_term', 'jobs')
def _get_jobs():
    dbsession = DBSession()
    jobs = dbsession.query(Job.prestige, Job.job).all()

def _get_employer_score(name):
    if _get_top_companies()[name]:
        return 500
    else:
        # Is basic score 200?
        return 200

@cache_region('long_term', 'top_companies')
def _get_top_companies():
    dbsession = DBSession()
    companies = dict.fromkeys(dbsession.query(Company.name).all(), 1)
    return companies

def _get_relationship_score(profile):
    try:
        return RELATIONSHIPS[profile['relationship_status']]
    except KeyError:
        return 1

def _get_family_score(profile):
    return 1

