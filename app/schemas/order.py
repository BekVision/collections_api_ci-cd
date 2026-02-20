from datetime import datetime

from app.schemas.common import BaseSchema
from app.schemas.product import ProductRead, ProductVariantRead


class OrderItemCreate(BaseSchema):
    product_id: int
    variant_id: int | None = None
    quantity: int


class OrderCreate(BaseSchema):
    items: list[OrderItemCreate]

    # ✅ NEW
    delivery_address_text: str
    delivery_lat: float | None = None
    delivery_lng: float | None = None
    delivery_note: str | None = None


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

    # ✅ NEW
    delivery_address_text: str | None
    delivery_lat: float | None
    delivery_lng: float | None
    delivery_note: str | None

    items: list[OrderItemRead]
    created_at: datetime


class OrderListResponse(BaseSchema):
    items: list[OrderRead]
    total: int
    skip: int
    limit: int
    next_skip: int | None

class OrderStatusUpdate(BaseSchema):
    status: str