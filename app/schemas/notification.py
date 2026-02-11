from datetime import datetime

from app.schemas.common import BaseSchema


class NotificationRead(BaseSchema):
    id: int
    type: str
    title: str
    body: str
    data: dict | None
    is_read: bool
    created_at: datetime
