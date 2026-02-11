from datetime import datetime
from app.schemas.common import BaseSchema


class CategoryCreate(BaseSchema):
    name: str
    icon_url: str | None = None  # (upload endpoint orqali ham yoziladi)


class CategoryUpdate(BaseSchema):
    name: str
    icon_url: str | None = None


class CategoryRead(BaseSchema):
    id: int
    name: str
    icon_url: str | None
    created_at: datetime


class CategoryListResponse(BaseSchema):
    items: list[CategoryRead]
    total: int
    skip: int
    limit: int
    next_skip: int | None
