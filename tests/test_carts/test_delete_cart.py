import pytest
from models.cart import DeletedCart
from models.error_response import ErrorResponse
from tests.test_carts.conftest import carts_client

# Падает c тем же багом по модели продукта описанном в test_get_cart_by_id
@pytest.mark.parametrize(('cart_id', 'expected_status_code'),
    [
        pytest.param(1, 200, id='Valid cart id')
    ]
)
def test_delete_cart_positive(carts_client, cart_id, expected_status_code):

    cart = carts_client.delete_cart(cart_id)

    assert cart.status_code == expected_status_code
    assert DeletedCart.model_validate(cart.json())

# Тут тест падает на пустом ИД, апи отдаёт все корзины при попытке удаления
# TODO завести баг чтобы возвращалась адекватная ошибка
@pytest.mark.parametrize(('cart_id', 'expected_status_code', 'expected_error_message'),
    [
        pytest.param(None, 404, "Cart with id 'None' not found", id='Nonexistent cart id'),
        pytest.param('', 404, "Cart with id '' not found", id='Empty cart id'),
        pytest.param('asdasd', 404, "Cart with id 'asdasd' not found", id='Invalid cart id')
    ]
)
def test_delete_cart_negative(carts_client, cart_id, expected_status_code, expected_error_message):
    cart = carts_client.delete_cart(cart_id)
    resp = cart.json()
    assert cart.status_code == expected_status_code

    assert resp['message'] == expected_error_message
    assert ErrorResponse.model_validate(resp)