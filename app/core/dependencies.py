from fastapi import Depends, Header, HTTPException
from sqlalchemy.orm import Session

from app.core.security import hash_api_key
from app.db.database import get_db
from app.db.models.api_key import ApiKey


def get_current_api_key(
    x_api_key: str | None = Header(default=None),
    db: Session = Depends(get_db),
) -> ApiKey:
    if not x_api_key:
        raise HTTPException(
            status_code=401,
            detail="Missing X-API-Key header",
        )

    hashed_key = hash_api_key(x_api_key)

    stored_key = (
        db.query(ApiKey)
        .filter(
            ApiKey.key_hash == hashed_key,
            ApiKey.is_active.is_(True),
        )
        .first()
    )

    if not stored_key:
        raise HTTPException(
            status_code=401,
            detail="Invalid or inactive API key",
        )

    return stored_key