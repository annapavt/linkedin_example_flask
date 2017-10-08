import pytest

from linkedin.app import create_app
from linkedin.init_db import init_db

@pytest.yield_fixture(scope='session')
def app():
    """
    Setup our flask test app, this only gets executed once.

    :return: Flask app
    """

    config = {
        'SERVER_NAME':'localhost',
        'SQLALCHEMY_DATABASE_URI':'sqlite:////tmp/mytest.db'

    }

    init_db(config)
    _app = create_app(config)

    # Establish an application context before running the tests.
    ctx = _app.app_context()
    ctx.push()

    yield _app

    ctx.pop()


@pytest.yield_fixture(scope='function')
def client(app):
    """
    Setup an app client, this gets executed for each test function.

    :param app: Pytest fixture
    :return: Flask app client
    """
    yield app.test_client()
