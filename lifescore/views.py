from pyramid.view import view_config

from lifescore.models import DBSession

@view_config(route_name='home', renderer='home.mak')
def my_view(request):
    dbsession = DBSession()
    settings = request.registry.settings
    fb_perms = ['user_education_history', 'friends_education_history',
                'publish_stream', 'offline_access',
                'user_relationships', 'friends_relationships',
                'user_work_history', 'friends_work_history',
                'user_location', 'friends_location']

    return dict(facebook_app_id=settings['facebook.app.id'], facebook_perms=\
                ','.join(fb_perms))
