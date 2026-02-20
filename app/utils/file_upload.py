import os
import uuid
from fastapi import UploadFile
import aiofiles

from app.core.config import get_settings

settings = get_settings()

MEDIA_DIR = "app/media"

async def save_file(file: UploadFile) -> str:
    os.makedirs(MEDIA_DIR, exist_ok=True)

    ext = (file.filename or "").split(".")[-1] if file.filename else "bin"
    filename = f"{uuid.uuid4()}.{ext}"
    path = os.path.join(MEDIA_DIR, filename)

    async with aiofiles.open(path, "wb") as out:
        await out.write(await file.read())

    # ✅ Mobil uchun to‘liq URL
    return f"{settings.public_base_url}/media/{filename}"