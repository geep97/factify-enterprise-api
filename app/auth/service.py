from datetime import datetime, timezone

from sqlalchemy.orm import Session, joinedload

from app.core.security import (
    decode_access_token,
    hash_api_key,
    verify_password,
)
from app.db.models.api_key import ApiKey
from app.db.models.user import User


class AuthenticationService:
    """
    Service responsible for authenticating API keys.
    """

    @staticmethod
    def authenticate(
        db: Session,
        api_key: str,
    ) -> ApiKey | None:
        """
        Authenticate an API key.

        Returns:
            Authenticated ApiKey if successful.
            None if invalid or inactive.
        """

        key_hash = hash_api_key(api_key)

        key = (
            db.query(ApiKey)
            .options(joinedload(ApiKey.organization))
            .filter(ApiKey.key_hash == key_hash)
            .first()
        )

        if key is None:
            return None

        if not key.is_active:
            return None

        key.last_used_at = datetime.now(timezone.utc)

        db.commit()

        return key


class UserAuthenticationService:
    """
    Service responsible for authenticating human users
    (email/password login and JWT access tokens).
    """

    @staticmethod
    def authenticate_credentials(
        db: Session,
        email: str,
        password: str,
    ) -> User | None:
        """
        Authenticate a user by email and password.

        Returns:
            Authenticated User if successful.
            None if invalid.
        """

        user = (
            db.query(User)
            .filter(User.email == email)
            .first()
        )

        if user is None:
            return None

        if not verify_password(password, user.hashed_password):
            return None

        return user

    @staticmethod
    def authenticate_token(
        db: Session,
        token: str,
    ) -> User | None:
        """
        Authenticate a user by JWT access token.

        Returns:
            Authenticated User if the token is valid.
            None if invalid, expired, or the user no longer exists.
        """

        payload = decode_access_token(token)

        if payload is None:
            return None

        user_id = payload.get("sub")

        if user_id is None:
            return None

        return (
            db.query(User)
            .filter(User.id == int(user_id))
            .first()
        )