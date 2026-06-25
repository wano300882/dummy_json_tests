import requests

from utils import config


class DummyJsonApiClient:
    def __init__(self):
        self.base_url = config.BASE_URL

        self.session = requests.Session()

        headers = {
            "Accept": "application/json"
        }

        self.session.headers.update(headers)

    def set_auth_token(self, token):
        self.session.headers.update({"Authorization": f"Bearer {token}"})

    def close(self):
        self.session.close()

    def clear_auth(self):
        self.session.headers.pop("Authorization", None)
        self.session.cookies.clear()

    def _url(self, path):
        return f"{self.base_url}{path}"

    def get(self, path, **kwargs):
        return self.session.get(self._url(path), **kwargs)

    def post(self, path, **kwargs):
        return self.session.post(self._url(path), **kwargs)

    def put(self, path, **kwargs):
        return self.session.put(self._url(path), **kwargs)

    def delete(self, path, **kwargs):
        return self.session.delete(self._url(path), **kwargs)


class UserAuthClient(DummyJsonApiClient):
    def login(self, username, password, expire_in_mins = 30):
        
        return self.post(f"/auth/login", json = {"username": username, "password": password, "expiresInMins": expire_in_mins})

    def get_user(self):
        return self.get(f"/auth/me")

class CartsClient(DummyJsonApiClient):

    def get_all_carts(self):
        return self.get("/carts")

    def get_cart_by_id(self, cart_id):
        return self.get(f"/carts/{cart_id}")

    def get_cart_by_user_id(self, user_id):
        return self.get(f"/carts/user/{user_id}")

    def create_cart(self, payload):
        return self.post(path=f"/carts/add", json=payload)

    def update_cart(self, cart_id, payload):
        return self.put(path=f"/carts/{cart_id}", json=payload)

    def delete_cart(self, cart_id):
        return self.delete(path=f"/carts/{cart_id}")
