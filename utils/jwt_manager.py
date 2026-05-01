import jwt
from datetime import datetime, timedelta, timezone
from typing import Optional
from core.config import settings


def create_access_token(
        data: dict,
        expires_delta: Optional[int] = None
):
    to_encode = data.copy()

    expire_minutes = expires_delta or settings.ACCESS_TOKEN_EXPIRE_MINUTES
    expire = datetime.now(timezone.utc) + timedelta(minutes=expire_minutes)

    to_encode.update({"exp": expire})

    return jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )


def create_refresh_token(
        data: dict,
        expires_delta: Optional[int] = None
):
    to_encode = data.copy()

    expire_minutes = expires_delta or settings.REFRESH_TOKEN_EXPIRE_MINUTES
    expire = datetime.now(timezone.utc) + timedelta(minutes=expire_minutes)

    to_encode.update({"exp": expire})

    return jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )


def verify_token(token: str):
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )
        return payload

    except jwt.ExpiredSignatureError:
        return None

    except jwt.PyJWTError:
        return None