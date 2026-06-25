import pytest
from models.cart import Cart
from models.error_response import ErrorResponse
from tests.test_carts.conftest import carts_client


@pytest.mark.parametrize('should_merge_products', [True, False])
@pytest.mark.parametrize(
    ('cart_id', 'products', 'expected_status_code'),
    [
        pytest.param(1, [(22, 1), (33, 2)], 200, id='Positive add cart multiple products, merge'),
        pytest.param(1, [(22, 1)], 200, id='Positive add cart single product, merge'),
        pytest.param(1, [], 200, id='Positive add cart empty product list, merge'),
    ]
)
def test_update_cart(cart_id, products, expected_status_code, carts_client, should_merge_products):
    products = [{'id': pid, 'quantity': qty} for pid, qty in products]
    payload = {'merge': should_merge_products,
               'products': products}
    cart = carts_client.update_cart(payload=payload, cart_id=cart_id)

    resp = cart.json()

    #TODO в боевых условиях я бы сделал эту проверку более детерминированной
    if not should_merge_products:
        assert len(resp['products']) == len(products)

    assert cart.status_code == expected_status_code
    assert Cart.model_validate(cart.json())



# Тесты с невалидными амаунтами и продуктИд падают ложно положительно, я бы предложил адекватную обработку таких кейсов
@pytest.mark.parametrize('should_merge_products', [True, False])
@pytest.mark.parametrize(
    ('cart_id', 'products', 'expected_status_code', 'expected_error_message'),
    [
        pytest.param(None, [(22, 1), (33, 2)], 404, "Cart with id 'None' not found", id='Negative update cart nonexistent cart id, merge'),
        pytest.param('invalid_cart_id', [(22, 1), (33, 2)], 404, "Cart with id 'invalid_cart_id' not found" , id='Negative update cart invalid cart id, merge'),
        pytest.param(1, [(22, '1')], 404, "Cart with id 'None' not found", id='Negative invalid product amount (str), merge'),
        pytest.param(1, [(22, None)], 404, "Cart with id 'None' not found", id='Negative invalid product amount (null), merge'),
        pytest.param(1, [('22', 1)], 404, "Cart with id 'None' not found", id='Negative invalid productId (str), merge'),
        pytest.param(1, [(None, 1)], 404, "Cart with id 'None' not found", id='Negative invalid productId (null), merge'),
    ]
)
def test_update_cart_negative(cart_id, products, expected_status_code, should_merge_products, expected_error_message, carts_client):
    payload = {'merge': should_merge_products,
               'products': products}

    cart = carts_client.update_cart(payload=payload, cart_id=cart_id)
    resp = cart.json()
    assert cart.status_code == expected_status_code
    assert resp['message'] == expected_error_message
    assert ErrorResponse.model_validate(resp)