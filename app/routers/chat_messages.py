from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session

from app.core.deps import get_current_user, get_db
from app.models.chat_message import ChatMessage
from app.models.notification import Notification
from app.schemas.chat_message import ChatMessageRead
from app.utils.file_upload import save_file

router = APIRouter(prefix="/chat", tags=["Chat"])


@router.get("/with/{user_id}", response_model=list[ChatMessageRead])
def get_chat_with_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return (
        db.query(ChatMessage)
        .filter(
            ((ChatMessage.sender_id == current_user.id) & (ChatMessage.receiver_id == user_id))
            | ((ChatMessage.sender_id == user_id) & (ChatMessage.receiver_id == current_user.id))
        )
        .order_by(ChatMessage.created_at.asc())
        .all()
    )


@router.post("/send", response_model=ChatMessageRead)
async def send_message(
    receiver_id: int = Form(...),
    message_type: str = Form(...),      # text/image/video/audio
    text: str | None = Form(None),      # text bo‘lsa
    file: UploadFile | None = File(None),  # media bo‘lsa
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    if message_type == "text":
        if not text:
            raise ValueError("text is required for message_type=text")
        content = text
    else:
        if not file:
            raise ValueError("file is required for media message")
        content = await save_file(file)

    msg = ChatMessage(
        sender_id=current_user.id,
        receiver_id=receiver_id,
        message_type=message_type,
        content=content,
    )
    db.add(msg)

    # ✅ receiver uchun notification
    db.add(
        Notification(
            recipient_user_id=receiver_id,
            type="chat_message",
            title="New message",
            body="You have a new message",
            data={"from_user_id": current_user.id},
        )
    )

    db.commit()
    db.refresh(msg)
    return msg
