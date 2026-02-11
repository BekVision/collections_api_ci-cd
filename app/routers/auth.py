from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.deps import get_db
from app.schemas.auth import RefreshTokenRequest, Token
from app.schemas.user import UserCreate, UserRead
from app.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register(payload: UserCreate, db: Session = Depends(get_db)):
    try:
        return AuthService(db).register(payload)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    try:
        access_token, refresh_token = AuthService(db).authenticate(
            form_data.username,
            form_data.password,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    return Token(access_token=access_token, refresh_token=refresh_token)


@router.post("/refresh", response_model=Token)
def refresh(payload: RefreshTokenRequest, db: Session = Depends(get_db)):
    try:
        access_token, refresh_token = AuthService(db).refresh_access_token(payload.refresh_token)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    return Token(access_token=access_token, refresh_token=refresh_token)
