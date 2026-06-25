import time

import pytest


@pytest.mark.parametrize(
    ('username', 'password', 'expected_status_code'),
    [
        pytest.param('michaelw', 'michaelwpass', 200, id='Get user data with correct token')
    ]
)
def test_user_data_positive(auth_client, username, password, expected_status_code):
    access_token = auth_client.login(username=username, password=password).json()['accessToken']
    auth_client.clear_auth()

    auth_client.set_auth_token(token=access_token)

    user_data = auth_client.get_user()

    # TODO проверка модели

    assert user_data.status_code == expected_status_code



@pytest.mark.parametrize(
    ('username', 'password', 'expected_status_code', 'token_should_exist', 'expected_error_message', 'token_expire_in_mins'),
    [
        pytest.param('michaelw', 'michaelwpass', 401, True, 'Token Expired!', 1, id='Get user data with expired token'),
        pytest.param('michaelw', 'michaelwpass', 401, False, 'Access Token is required', None, id='Get user data without token'),
    ]
)
def test_user_data_negative(auth_client, username, password, expected_status_code, token_should_exist, expected_error_message, token_expire_in_mins):
    access_token = auth_client.login(username=username, password=password, expire_in_mins=token_expire_in_mins).json()['accessToken']
    auth_client.clear_auth()

    if token_expire_in_mins:
        time.sleep(token_expire_in_mins * 60 + 5)

    if token_should_exist:
        auth_client.set_auth_token(token=access_token)

    user_data = auth_client.get_user()

    assert user_data.status_code == expected_status_code
    assert user_data.json()['message'] == expected_error_message
