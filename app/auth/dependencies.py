from fastapi import Depends, Header, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.auth.service import AuthenticationService, UserAuthenticationService
from app.db.database import get_db
from app.db.models.api_key import ApiKey
from app.db.models.organization import Organization
from app.db.models.user import User

bearer_scheme = HTTPBearer()


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
    Return the authenticated organization (API key auth only).
    """

    return api_key.organization


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> User:
    """
    Authenticate the incoming request via JWT access token
    and return the authenticated user.
    """

    user = UserAuthenticationService.authenticate_token(
        db=db,
        token=credentials.credentials,
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token.",
        )

    return user


def get_current_organization_any(
    x_api_key: str | None = Header(
        default=None,
        alias="X-API-Key",
    ),
    authorization: str | None = Header(default=None),
    db: Session = Depends(get_db),
) -> Organization:
    """
    Authenticate the incoming request via EITHER an API key
    (X-API-Key header) OR a login token (Authorization: Bearer),
    and return the authenticated organization.

    Used for actions that only need proof of organization
    ownership, not a specific credential type (e.g. creating
    an additional API key).
    """

    if x_api_key is not None:
        api_key = AuthenticationService.authenticate(
            db=db,
            api_key=x_api_key,
        )

        if api_key is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or inactive API key.",
            )

        return api_key.organization

    if authorization is not None and authorization.lower().startswith("bearer "):
        token = authorization.split(" ", 1)[1]

        user = UserAuthenticationService.authenticate_token(
            db=db,
            token=token,
        )

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token.",
            )

        organization = (
            db.query(Organization)
            .filter(Organization.id == user.organization_id)
            .first()
        )

        if organization is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Organization not found.",
            )

        return organization

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Missing credentials. Provide X-API-Key or Authorization: Bearer <token>.",
    )