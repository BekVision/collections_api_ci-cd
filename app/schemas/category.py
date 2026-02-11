from datetime import datetime

from app.schemas.common import BaseSchema


class CategoryCreate(BaseSchema):
    name: str


class CategoryUpdate(BaseSchema):
    name: str


class CategoryRead(BaseSchema):
    id: int
    name: str
    created_at: datetime


class CategoryListResponse(BaseSchema):
    items: list[CategoryRead]
    total: int
    skip: int
    limit: int
    next_skip: int | None
