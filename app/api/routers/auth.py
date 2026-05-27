from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
import hashlib
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.auth.security import hash_password, verify_password
from app.services.auth.jwt_token import create_access_and_refresh_token, get_user_from_token, validate_token
from app.core.config import settings
from app.models.refresh_token import RefreshToken
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin, AuthResponse

router = APIRouter(prefix="/auth", tags=["auth"])

DbSession = Annotated[Session, Depends(get_db)]


def _hash_refresh_token(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def _extract_token_expiration(token: str) -> datetime:
    payload = validate_token(token)
    exp = payload.get("exp")
    if exp is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has no expiration.",
        )
    return datetime.fromtimestamp(int(exp), tz=timezone.utc)


def _as_utc(dt: datetime) -> datetime:
    # Some DB drivers return naive datetimes; treat them as UTC.
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def _save_refresh_token(db: Session, user: User, refresh_token: str) -> None:
    db.add(
        RefreshToken(
            user_id=user.id,
            token_hash=_hash_refresh_token(refresh_token),
            expires_at=_extract_token_expiration(refresh_token),
        )
    )


def _get_active_refresh_token(db: Session, raw_refresh_token: str) -> RefreshToken | None:
    token_hash = _hash_refresh_token(raw_refresh_token)
    return db.scalar(
        select(RefreshToken).where(
            RefreshToken.token_hash == token_hash,
            RefreshToken.revoked_at.is_(None),
        )
    )


def _set_refresh_cookie(response: Response, refresh_token: str) -> None:
    response.set_cookie(
        key=settings.REFRESH_COOKIE_NAME,
        value=refresh_token,
        httponly=True,
        secure=settings.REFRESH_COOKIE_SECURE,
        samesite=settings.REFRESH_COOKIE_SAMESITE,
        max_age=settings.JWT_REFRESH_TOKEN_TTL_MINUTES * 60,
        path="/auth",
    )


def _delete_refresh_cookie(response: Response) -> None:
    response.delete_cookie(key=settings.REFRESH_COOKIE_NAME, path="/auth")

@router.post(
    "/signup/",
    response_model=AuthResponse,
    status_code=status.HTTP_201_CREATED,
)
def signup(payload: UserCreate, db: DbSession, response: Response) -> AuthResponse:
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

    access_token, new_refresh_token = create_access_and_refresh_token(user=user)
    _save_refresh_token(db, user, new_refresh_token)
    db.commit()

    _set_refresh_cookie(response, new_refresh_token)
    return AuthResponse(
        access_token=access_token,
        user=user,
    )


@router.post(
    "/login/",
    response_model=AuthResponse,
    status_code=status.HTTP_200_OK,
)
def login(payload: UserLogin, db: DbSession, response: Response) -> AuthResponse:
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

    access_token, new_refresh_token = create_access_and_refresh_token(user=user)
    _save_refresh_token(db, user, new_refresh_token)
    db.commit()
    _set_refresh_cookie(response, new_refresh_token)

    return AuthResponse(
        access_token=access_token,
        user=user,
    )


@router.post(
    "/refresh/",
    response_model=AuthResponse,
    status_code=status.HTTP_200_OK,
)
def refresh_token(request: Request, response: Response, db: DbSession) -> AuthResponse:
    raw_refresh_token = request.cookies.get(settings.REFRESH_COOKIE_NAME)
    if not raw_refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing refresh token cookie",
        )

    stored_token = _get_active_refresh_token(db, raw_refresh_token)
    if stored_token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token is revoked or unknown",
        )

    if _as_utc(stored_token.expires_at) <= datetime.now(timezone.utc):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token has expired",
        )

    user = get_user_from_token(
        token=raw_refresh_token,
        db=db,
        expected_token_type="refresh",
    )

    stored_token.revoked_at = datetime.now(timezone.utc)

    access_token, new_refresh_token = create_access_and_refresh_token(user=user)
    _save_refresh_token(db, user, new_refresh_token)
    db.commit()
    _set_refresh_cookie(response, new_refresh_token)

    return AuthResponse(
        access_token=access_token,
        user=user,
    )


@router.post(
    "/logout/",
    status_code=status.HTTP_204_NO_CONTENT,
)
def logout(request: Request, response: Response, db: DbSession) -> Response:
    raw_refresh_token = request.cookies.get(settings.REFRESH_COOKIE_NAME)
    if not raw_refresh_token:
        _delete_refresh_cookie(response)
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    stored_token = _get_active_refresh_token(db, raw_refresh_token)
    if stored_token is None:
        _delete_refresh_cookie(response)
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    stored_token.revoked_at = datetime.now(timezone.utc)
    db.commit()
    _delete_refresh_cookie(response)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
