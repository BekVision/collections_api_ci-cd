from datetime import datetime

from app.schemas.common import BaseSchema
from app.schemas.category import CategoryRead


class ProductImageRead(BaseSchema):
    id: int
    url: str


class ProductVariantCreate(BaseSchema):
    name: str
    price: float


class ProductVariantRead(BaseSchema):
    id: int
    name: str
    price: float


class ProductCreate(BaseSchema):
    name: str
    description: str
    price: float
    rating: float = 0
    category_id: int
    images: list[str] = []
    variants: list[ProductVariantCreate] = []


class ProductUpdate(BaseSchema):
    name: str | None = None
    description: str | None = None
    price: float | None = None
    rating: float | None = None
    category_id: int | None = None
    images: list[str] | None = None
    variants: list[ProductVariantCreate] | None = None


class ProductRead(BaseSchema):
    id: int
    name: str
    description: str
    price: float
    rating: float
    category: CategoryRead
    images: list[ProductImageRead]
    variants: list[ProductVariantRead]
    views_count: int
    sold_count: int
    created_at: datetime


class ProductListResponse(BaseSchema):
    items: list[ProductRead]
    total: int
    skip: int
    limit: int
    next_skip: int | None
