from models.base import StrictBaseModel


class ErrorResponse(StrictBaseModel):
    message: str