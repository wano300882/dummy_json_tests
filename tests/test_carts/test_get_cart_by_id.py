import pytest
from models.cart import Cart



# Тут тест падает на валидации модели, почему-то апи отдаёт другую модель продукта между разными
# эндпоинтами в /add возвращается discountedPrice в get в модели продукта возвращается discountedTotal
# TODO завести баг
@pytest.mark.parametrize(('cart_id', 'expected_status_code'),
    [
        pytest.param(1, 200, id='Valid cart id')
    ]
)
def test_get_cart_by_id(carts_client, cart_id, expected_status_code):
    cart = carts_client.get_cart_by_id(cart_id)

    assert cart.status_code == expected_status_code
    assert Cart.model_validate(cart.json())

# Тут тест падает на пустом ИД, апи отдаёт все корзины при пустом инпуте
# TODO завести баг
@pytest.mark.parametrize(('cart_id', 'expected_status_code', 'expected_error_message'),
    [
        pytest.param(None, 404, "Cart with id 'None' not found", id='Nonexistent cart id'),
        pytest.param('', 404, "Cart with id '' not found", id='Empty cart id'),
        pytest.param('asdasd', 404, "Cart with id 'asdasd' not found", id='Invalid cart id')
    ]
)
def test_get_cart_by_id_negative(carts_client, cart_id, expected_status_code, expected_error_message):
    cart = carts_client.get_cart_by_id(cart_id)
    assert cart.status_code == expected_status_code
    assert cart.json()['message'] == expected_error_message