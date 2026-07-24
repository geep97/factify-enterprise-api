from datetime import datetime, timezone

from sqlalchemy.orm import Session, joinedload

from app.core.security import hash_api_key
from app.db.models.api_key import ApiKey


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