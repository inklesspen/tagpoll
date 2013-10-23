import os
import warnings
import sqlalchemy
import pytest
import transaction

from pyramid.paster import (
    get_appsettings,
    setup_logging,
)

from ..models import (
    DBSession,
    Base
)


@pytest.fixture(scope='session', autouse=True)
def set_sqlalchemy_warnings_as_errors(request):
    warnings.simplefilter('error', category=sqlalchemy.exc.SAWarning)


@pytest.fixture(scope='session')
def config_uri(request):
    config_uri = os.path.abspath(request.config.option.ini)
    return config_uri


@pytest.fixture(scope='session')
def appsettings(config_uri):
    setup_logging(config_uri)
    settings = get_appsettings(config_uri)
    return settings


@pytest.fixture(scope='session')
def sqlengine(request, appsettings):
    engine = sqlalchemy.engine_from_config(appsettings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    return engine


@pytest.fixture()
def dbtables(request, sqlengine):
    Base.metadata.create_all(sqlengine)

    def teardown():
        transaction.abort()
        Base.metadata.drop_all(sqlengine)

    request.addfinalizer(teardown)


def pytest_addoption(parser):
    parser.addoption("--ini", action="store", metavar="INI_FILE", help="use INI_FILE to configure SQLAlchemy")
