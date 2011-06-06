from pyramid_beaker import set_cache_regions_from_settings
from pyramid_beaker import session_factory_from_settings
from pyramid.config import Configurator
from sqlalchemy import engine_from_config

from lifescore.models import initialize_sql

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    initialize_sql(engine)
    set_cache_regions_from_settings(settings)
    session_factory = session_factory_from_settings(settings)
    config = Configurator(settings=settings)
    config.set_session_factory(session_factory)
    config.scan()
    config.add_static_view('static', 'lifescore:static')
    config.add_route('home', '/')
    config.add_route('dashboard', '/profile/{fb_id}')
    config.add_route('fetch_friends', '/fetch_friends')
    return config.make_wsgi_app()


