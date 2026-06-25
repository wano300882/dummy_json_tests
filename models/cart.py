from pydantic import HttpUrl

from models.base import StrictBaseModel


class CartProduct(StrictBaseModel):
    id: int
    title: str
    price: float
    quantity: int
    total: float
    discountPercentage: float
    discountedPrice: float
    thumbnail: HttpUrl


class Cart(StrictBaseModel):
    id: int
    products: list[CartProduct]
    total: float
    discountedTotal: float
    userId: int
    totalProducts: int
    totalQuantity: int

class DeletedCart(Cart):
    isDeleted: bool
    deletedOn: str