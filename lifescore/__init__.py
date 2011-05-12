from pyramid.config import Configurator
from sqlalchemy import engine_from_config

from lifescore.models import initialize_sql

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    initialize_sql(engine)
    config = Configurator(settings=settings)
    config.scan()
    config.add_static_view('static', 'lifescore:static')
    config.add_route('home', '/')
    return config.make_wsgi_app()


