import facebook
from pyramid.view import view_config
from pyramid.url import route_url

from lifescore.models import User
from lifescore.models import DBSession

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
        print 'cookie is here'
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
        graph = facebook.GraphAPI(cookie['access_token'])
        profile = graph.get_object('me')
        fb_id = profile['id']
        user = dbsession.query(User).filter(User.fb_id==fb_id).first()
        if not user:
            user = User(fb_id, cookie['access_token'], profile['updated_time'],
                       get_lifescore(profile))
            dbsession.add(user)
            dbsession.commit()
            print get_friends_id(graph)
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
    pass

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
    #schools = profile['education']
    ## if you do not have the information, the key does not exist
    #employers = profile['work']
    #relationship = profile['relationship_status']
    #location = profile['location']
    #gender = profile['gender']
    return 1

