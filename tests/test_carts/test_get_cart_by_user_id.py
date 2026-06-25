import pytest

@pytest.fixture(
                params=[(1, 200), (None, 400), ('asdasd', 400)],
                ids=['Valid user id', 'Nonexistent user id', 'Invalid user id']
                )
def get_testing_user_id(request):
    return {'user_id': request.param[0], 'expected_status_code': request.param[1]}

def test_get_cart_by_user_id(get_testing_user_id, carts_client):
    user_id = get_testing_user_id['user_id']
    expected_status_code = get_testing_user_id['expected_status_code']

    assert carts_client.get_cart_by_user_id(user_id).status_code == expected_status_code