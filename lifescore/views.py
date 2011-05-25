import random

from beaker.cache import cache_region
import facebook
import memcache
from pyramid.view import view_config
from pyramid.url import route_url

from lifescore.models import User, NationalSchools, WorldSchools
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
        graph = get_graph(cookie['access_token'])
        profile = graph.get_object('me')
        fb_id = profile['id']
        user = dbsession.query(User).filter(User.fb_id==fb_id).first()
        if not user:
            user = User(fb_id, cookie['access_token'], profile['updated_time'],
                       get_lifescore(profile), )
            dbsession.add(user)
            dbsession.commit()
            return dict(fb_id=fb_id,
                        friends_id=get_friends_id(graph).encode('ascii', 'ignore'))
        elif user.fb_access_token != cookie['access_token']:
            user.fb_access_token = cookie['access_token']
            if user.fb_updated_time != profile['update_time']:
                user.score = get_lifescore(profile)
            dbsession.merge(user)
            dbsession.commit()
            #fecth existing data from db and return the dashboard
    else:
        # need redirect to a 404 error page
        fb_id = 'no cookie'
        pass
    
    return dict(fb_id=fb_id)

@view_config(route_name='fetch_friends', renderer='json')
def fetch_friends(request):
    friends_id = request.GET['friends_id']
    user = get_user_from_fb_id(request.GET['fb_id'])
    graph = get_graph(user.fb_access_token)
    friends = graph.get_objects(friends_id.split(','))
    return [dict(id=f['id'], score=get_lifescore(f)) for f in
            friends.itervalues()]

@cache_region('short_term', 'graph')
def get_graph(access_token):
    return facebook.GraphAPI(access_token)

@cache_region('short_term', 'user_in_db')
def get_user_from_fb_id(fb_id):
    dbsession = DBSession()
    return dbsession.query(User).filter(User.fb_id==fb_id).first()

def get_friends_id(graph):
    return ','.join([f['id'] for f in graph.get_connections('me',
                                                            'friends')['data']])

def get_lifescore_influenced(graph):
    score = get_lifescore(graph.get_object('me'))
    friends = graph.get_connections('me', 'friends')['data']
    for f in friends:
        score += get_lifescore(graph.get_object(f['id']))
    return score

def get_lifescore(profile):
    score = (get_education_score(profile) + get_work_score(profile)) * \
            get_relationship_score(profile) * get_family_score(profile)
    #location = profile['location']
    #gender = profile['gender']
    return random.randint(400, 850)

def get_education_score(profile):
    try:
        schools = profile['education']
        return 0
    except KeyError:
        return 0

@cache_region('long_term', 'single_school_rank')
def get_school_rank(name):
    try:
        rank = get_all_national_schools()['names'].index(name)
    except ValueError:
        try:
            rank = get_all_national_schools()['short_names'].index(name)
        except ValueError:
            try:
                rank = get_all_world_schools()['names'].index(name)
            except ValueError:
                try:
                    rank = get_all_world_schools()['short_names'].index(name)
                except ValueError:
                    return 0
    return 500 - rank

@cache_region('long_term', 'world_schools')
def get_all_world_schools():
    dbsession = DBSession()
    schools = dbsession.query(WorldSchools.rank, WorldSchools.name,
                    WorldSchools.short_name).all()
    names = [s.name for s in schools]
    short_names = [s.short_name for s in schools]
    return dict(names=names, short_names=short_names)

@cache_region('long_term', 'national_schools')
def get_all_national_schools():
    dbsession = DBSession()
    schools = dbsession.query(NationalSchools.rank, NationalSchools.name,
                    NationalSchools.short_name).all()
    names = [s.name for s in schools]
    short_names = [s.short_name for s in schools]
    return dict(names=names, short_names=short_names)

def get_work_score(profile):
    try:
        employers = profile['work']
        return 0
    except KeyError:
        return 0;

def get_relationship_score(profile):
    try:
        return RELATIONSHIPS[profile['relationship_status']]
    except KeyError:
        return 1

def get_family_score(profile):
    return 1

