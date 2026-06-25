from pydantic import HttpUrl

from models.base import StrictBaseModel


class AuthUser(StrictBaseModel):
    id: int
    username: str
    email: str
    firstName: str
    lastName: str
    gender: str
    image: HttpUrl
    accessToken: str
    refreshToken: str


