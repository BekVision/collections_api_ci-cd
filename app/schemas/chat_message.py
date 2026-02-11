from datetime import datetime

from app.schemas.common import BaseSchema


class ChatMessageCreate(BaseSchema):
    receiver_id: int
    message_type: str  # text/image/video/audio
    content: str       # text yoki file_url


class ChatMessageRead(BaseSchema):
    id: int
    sender_id: int
    receiver_id: int
    message_type: str
    content: str
    created_at: datetime
