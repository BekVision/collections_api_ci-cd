from datetime import datetime

from pydantic import EmailStr, Field

from app.schemas.common import BaseSchema


class UserCreate(BaseSchema):
    email: EmailStr
    password: str = Field(min_length=8)
    is_admin: bool = False


class UserUpdate(BaseSchema):
    is_active: bool | None = None
    is_admin: bool | None = None


class UserSelfUpdate(BaseSchema):
    email: EmailStr | None = None
    password: str | None = Field(default=None, min_length=8)


class UserRead(BaseSchema):
    id: int
    email: EmailStr
    is_admin: bool
    is_active: bool
    created_at: datetime
