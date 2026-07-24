from fastapi import Depends, Header, HTTPException
from sqlalchemy.orm import Session

from app.core.security import hash_api_key
from app.db.database import get_db
from app.repositories.api_key_repository import ApiKeyRepository


def get_current_api_key(
    x_api_key: str | None = Header(default=None),
    db: Session = Depends(get_db),
):
    if not x_api_key:
        raise HTTPException(
            status_code=401,
            detail="Missing X-API-Key header",
        )

    hashed_key = hash_api_key(x_api_key)

    repo = ApiKeyRepository(db)

    stored_key = repo.find_active_by_hash(hashed_key)

    if not stored_key:
        raise HTTPException(
            status_code=401,
            detail="Invalid or inactive API key",
        )

    repo.update_last_used(stored_key)

    return stored_key