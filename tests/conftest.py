import pytest
from faker import Faker

from webapp import create_app


def pytest_make_parametrize_id(config, val):  # noqa: W0613
    return repr(val)


@pytest.fixture()
def client(mocker):
    mocker.patch('sentry_sdk.init')
    mocker.patch('os.environ')
    mocker.patch('sqlalchemy.create_engine')
    app = create_app()
    return app.test_client()


@pytest.fixture(scope='session')
def fake():
    return Faker()
