from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.repositories.user import UserRepository
from app.schemas.user import UserSelfUpdate, UserUpdate


class UserService:
    def __init__(self, db: Session):
        self.user_repo = UserRepository(db)

    def list_users(self, skip: int, limit: int):
        return self.user_repo.list(skip=skip, limit=limit)

    def get_user(self, user_id: int):
        return self.user_repo.get_by_id(user_id)

    def update_user(self, user_id: int, payload: UserUpdate):
        user = self.user_repo.get_by_id(user_id)
        if not user:
            return None
        if payload.is_active is not None:
            user.is_active = payload.is_active
        if payload.is_admin is not None:
            user.is_admin = payload.is_admin
        return self.user_repo.update(user)

    def update_me(self, user_id: int, payload: UserSelfUpdate):
        user = self.user_repo.get_by_id(user_id)
        if not user:
            return None
        if payload.email is not None:
            existing = self.user_repo.get_by_email(payload.email)
            if existing and existing.id != user_id:
                raise ValueError("Email already registered")
            user.email = payload.email
        if payload.password is not None:
            user.hashed_password = hash_password(payload.password)
        return self.user_repo.update(user)

    def delete_user(self, user_id: int) -> bool:
        user = self.user_repo.get_by_id(user_id)
        if not user:
            return False
        self.user_repo.delete(user)
        return True
