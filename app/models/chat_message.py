from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id: Mapped[int] = mapped_column(primary_key=True)

    sender_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    receiver_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)

    message_type: Mapped[str] = mapped_column(String(20))  # text/image/video/audio
    content: Mapped[str] = mapped_column(String)           # text yoki file_url

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
