import pytest

from utils.api_client import UserAuthClient


@pytest.fixture()
def auth_client():
    client = UserAuthClient()
    yield client
    client.close()
