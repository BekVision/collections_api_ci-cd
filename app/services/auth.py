from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.security import create_access_token, create_refresh_token, hash_password, verify_password
from app.models.user import User
from app.repositories.user import UserRepository
from app.schemas.user import UserCreate


class AuthService:
    def __init__(self, db: Session):
        self.db = db
        self.user_repo = UserRepository(db)

    def register(self, payload: UserCreate) -> User:
        existing = self.user_repo.get_by_email(payload.email)
        if existing:
            raise ValueError("Email already registered")

        raw = payload.password
        # SecretStr bo‘lsa ichidagi qiymatni oladi, bo‘lmasa o‘sha str qoladi
        if hasattr(raw, "get_secret_value"):
            raw = raw.get_secret_value()

        # bcrypt 72 bytes limit -> UTF-8 bo‘yicha truncate
        raw_bytes = raw.encode("utf-8")
        if len(raw_bytes) > 72:
            raw = raw_bytes[:72].decode("utf-8", errors="ignore")

        user = User(
            email=payload.email,
            hashed_password=hash_password(raw),
            is_admin=payload.is_admin,
        )
        return self.user_repo.create(user)

    def authenticate(self, email: str, password: str) -> tuple[str, str]:
        user = self.user_repo.get_by_email(email)
        if not user or not verify_password(password, user.hashed_password):
            raise ValueError("Invalid credentials")
        return create_access_token(user.email), create_refresh_token(user.email)

    def refresh_access_token(self, refresh_token: str) -> tuple[str, str]:
        settings = get_settings()
        try:
            payload = jwt.decode(refresh_token, settings.secret_key, algorithms=[settings.algorithm])
        except JWTError as exc:
            raise ValueError("Invalid refresh token") from exc

        token_type = payload.get("type")
        subject = payload.get("sub")
        if token_type != "refresh" or not subject:
            raise ValueError("Invalid refresh token")

        return create_access_token(subject), create_refresh_token(subject)
