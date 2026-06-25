import pytest
import allure
from models.auth_user import AuthUser
from models.error_response import ErrorResponse


@allure.story('User authorization')
@pytest.mark.parametrize(
    ('username', 'password', 'expected_status_code'),
    [
        ('michaelw','michaelwpass',200)
    ],
    ids=['Successful auth'])
def test_user_login_positive(auth_client, username, password, expected_status_code):
    user_login = auth_client.login(username=username, password=password)

    with allure.step('Verify authorization status code'):
        assert user_login.status_code == expected_status_code

    with allure.step('Verify response json schema'):
        assert AuthUser.model_validate(user_login.json())




@allure.story('User authorization')
@pytest.mark.parametrize(
    ('username', 'password', 'expected_status_code', 'expected_error_message'),
    [
        ('michaelwasd', 'michaelwrongpass', 400, 'Invalid credentials'),
        (None, 'michaelwrongpass', 400, 'Username and password required'),
        ('', 'michaelwrongpass', 400, 'Username and password required'),
        ('michaelwasd', None, 400, 'Username and password required'),
        ('michaelwasd', '', 400, 'Username and password required')
    ],
    ids=['Wrong login/pass', 'Null username', 'Empty username', 'Null password', 'Empty password'])
def test_user_login_negative(auth_client, username, password, expected_status_code, expected_error_message):
    user_login = auth_client.login(username=username, password=password)

    with allure.step('Verify authorization status code'):
        assert user_login.status_code == expected_status_code

    with allure.step('Verify response json schema'):
        assert ErrorResponse.model_validate(user_login.json())

    with allure.step('Check error message'):
        assert user_login.json()['message'] == expected_error_message
