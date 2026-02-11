from datetime import datetime

from app.schemas.common import BaseSchema
from app.schemas.product import ProductRead, ProductVariantRead


class OrderItemCreate(BaseSchema):
    product_id: int
    variant_id: int | None = None
    quantity: int


class OrderCreate(BaseSchema):
    items: list[OrderItemCreate]


class OrderItemRead(BaseSchema):
    id: int
    product: ProductRead
    variant: ProductVariantRead | None = None
    quantity: int
    unit_price: float
    created_at: datetime


class OrderRead(BaseSchema):
    id: int
    status: str
    items: list[OrderItemRead]
    created_at: datetime


class OrderListResponse(BaseSchema):
    items: list[OrderRead]
    total: int
    skip: int
    limit: int
    next_skip: int | None
