import pytest
from models.cart import Cart
from models.error_response import ErrorResponse
from tests.test_carts.conftest import carts_client


@pytest.mark.parametrize(
    ('user_id', 'products', 'expected_status_code'),
    [
        pytest.param(1, [(22, 1), (33, 2)], 201, id='Positive add cart multiple products'),
        pytest.param(1, [(22, 1)], 201, id='Positive add cart single product')
    ]
)
def test_add_cart(user_id, products, expected_status_code, carts_client):
    payload = {'userId': user_id,
               'products': [{'id': pid, 'quantity': qty} for pid, qty in products]}
    cart = carts_client.create_cart(payload=payload)

    assert cart.status_code == expected_status_code
    assert Cart.model_validate(cart.json())


@pytest.mark.parametrize(
    ('user_id', 'products', 'expected_status_code', 'expected_error_message'),
    [
        pytest.param(1, [], 400, 'products can not be empty', id='Negative add empty cart'),
        pytest.param(None, [(22, 1), (33, 2)], 400, 'User id is required', id='Negative add cart nonexistent user id'),
        pytest.param('invalid_user_id', [(22, 1), (33, 2)], 400, "Invalid user id 'invalid_user_id'" , id='Negative add cart invalid user id')
    ]
)
def test_add_cart_negative(user_id, products, expected_status_code, expected_error_message, carts_client):
    payload = {'userId': user_id,
               'products': [{'id': pid, 'quantity': qty} for pid, qty in products]}

    cart = carts_client.create_cart(payload=payload)
    resp = cart.json()

    assert cart.status_code == expected_status_code
    assert resp['message'] == expected_error_message
    assert ErrorResponse.model_validate(resp)