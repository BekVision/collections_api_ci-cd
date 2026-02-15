from __future__ import annotations

from datetime import datetime

from app.schemas.common import BaseSchema


class ProductRatingUpsert(BaseSchema):
    rating: int  # 1..5 (validated in router)


class ProductRatingStats(BaseSchema):
    product_id: int
    average: float
    count: int


class ProductRatingMy(BaseSchema):
    product_id: int
    rating: int | None


class ProductCommentCreate(BaseSchema):
    text: str


class ProductCommentRead(BaseSchema):
    id: int
    product_id: int
    user_id: int
    text: str
    created_at: datetime


class ProductCommentListResponse(BaseSchema):
    items: list[ProductCommentRead]
    total: int
    skip: int
    limit: int
    next_skip: int | None
