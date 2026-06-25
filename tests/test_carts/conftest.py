import pytest

from utils.api_client import CartsClient


"""
5. Получение корзин пользователя:
GET /carts/user/{userId}

6. Получение корзины по id:
GET /carts/{cartId}

7. Создание корзины:
POST /carts/add

8. Обновление корзины:
PUT или PATCH /carts/{cartId}

9. Удаление корзины:
DELETE /carts/{cartId}
"""

@pytest.fixture()
def carts_client():
    client = CartsClient()
    yield client
    client.close()





