import hashlib
import secrets

from app.core.config import settings


def generate_api_key() -> str:
    random_part = secrets.token_urlsafe(32)

    return f"{settings.API_KEY_PREFIX}{random_part}"


def hash_api_key(api_key: str) -> str:
    return hashlib.sha256(
        api_key.encode("utf-8")
    ).hexdigest()


def get_key_prefix(api_key: str) -> str:
    return api_key[: len(settings.API_KEY_PREFIX) + 8]