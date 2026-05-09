from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.auth.security import hash_password, verify_password
from app.services.auth.jwt_token import create_access_and_refresh_token
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin, AuthResponse

router = APIRouter(prefix="/auth", tags=["auth"])

DbSession = Annotated[Session, Depends(get_db)]

@router.post(
    "/signup/",
    response_model=AuthResponse,
    status_code=status.HTTP_201_CREATED,
)
def signup(payload: UserCreate, db: DbSession) -> AuthResponse:
    existing_user = db.query(User).filter(User.email == payload.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists",
        )

    user = User(
        email=payload.email,
        hashed_password=hash_password(payload.password),
        first_name=payload.first_name,
        last_name=payload.last_name,
        is_active=True,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    access_token, refresh_token = create_access_and_refresh_token(user=user)

    return AuthResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        user=user,
    )


@router.post(
    "/login/",
    response_model=AuthResponse,
    status_code=status.HTTP_200_OK,
)
def login(payload: UserLogin, db: DbSession) -> AuthResponse:
    user = db.query(User).filter(User.email == payload.email).first()

    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is inactive",
        )

    access_token, refresh_token = create_access_and_refresh_token(user=user)

    return AuthResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        user=user,
    )

#TODO logout