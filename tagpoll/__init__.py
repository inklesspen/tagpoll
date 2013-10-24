from pyramid.config import Configurator
from sqlalchemy import engine_from_config
from pyramid.session import UnencryptedCookieSessionFactoryConfig

from .models import (
    DBSession,
    Base,
)


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine

    session_timeout = 86400 * 20
    my_session_factory = UnencryptedCookieSessionFactoryConfig(settings['session.secret'], timeout=session_timeout, cookie_max_age=session_timeout)

    config = Configurator(settings=settings)
    config.set_session_factory(my_session_factory)
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.include('tagpoll.views')
    return config.make_wsgi_app()
