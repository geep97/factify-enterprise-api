import hashlib
import secrets
from datetime import datetime, timedelta, timezone

import bcrypt
import jwt

from app.core.config import settings


# ============================================================
# API KEYS
# ============================================================

def generate_api_key() -> str:
    random_part = secrets.token_urlsafe(32)

    return f"{settings.API_KEY_PREFIX}{random_part}"


def hash_api_key(api_key: str) -> str:
    return hashlib.sha256(
        api_key.encode("utf-8")
    ).hexdigest()


def get_key_prefix(api_key: str) -> str:
    return api_key[: len(settings.API_KEY_PREFIX) + 8]


# ============================================================
# PASSWORDS
# ============================================================

def hash_password(password: str) -> str:
    hashed = bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt(),
    )

    return hashed.decode("utf-8")


def verify_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(
        password.encode("utf-8"),
        hashed_password.encode("utf-8"),
    )


# ============================================================
# JWT ACCESS TOKENS
# ============================================================

def create_access_token(data: dict) -> str:
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.JWT_EXPIRE_MINUTES
    )

    to_encode.update({"exp": expire})

    return jwt.encode(
        to_encode,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )


def decode_access_token(token: str) -> dict | None:
    try:
        return jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
        )
    except jwt.PyJWTError:
        return None