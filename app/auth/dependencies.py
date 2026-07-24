from fastapi import Depends, Header, HTTPException, status
from sqlalchemy.orm import Session

from app.auth.service import AuthenticationService
from app.db.database import get_db
from app.db.models.api_key import ApiKey
from app.db.models.organization import Organization


def get_current_api_key(
    x_api_key: str | None = Header(
        default=None,
        alias="X-API-Key",
    ),
    db: Session = Depends(get_db),
) -> ApiKey:
    """
    Authenticate the incoming request and return
    the authenticated API key.
    """

    if x_api_key is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing API key.",
        )

    api_key = AuthenticationService.authenticate(
        db=db,
        api_key=x_api_key,
    )

    if api_key is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or inactive API key.",
        )

    return api_key


def get_current_organization(
    api_key: ApiKey = Depends(get_current_api_key),
) -> Organization:
    """
    Return the authenticated organization.
    """

    return api_key.organization