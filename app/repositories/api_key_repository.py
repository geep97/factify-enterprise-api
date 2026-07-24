from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.db.models.api_key import ApiKey


class ApiKeyRepository:
    def __init__(self, db: Session):
        self.db = db

    # ============================================================
    # CREATE
    # ============================================================

    def create(self, api_key: ApiKey):
        self.db.add(api_key)
        return api_key

    # ============================================================
    # READ
    # ============================================================

    def find_active_by_hash(self, key_hash: str):
        return (
            self.db.query(ApiKey)
            .filter(
                ApiKey.key_hash == key_hash,
                ApiKey.is_active.is_(True),
            )
            .first()
        )

    def get_by_id(self, key_id: int):
        return (
            self.db.query(ApiKey)
            .filter(ApiKey.id == key_id)
            .first()
        )

    def list_by_organization(self, organization_id: int):
        return (
            self.db.query(ApiKey)
            .filter(ApiKey.organization_id == organization_id)
            .order_by(ApiKey.created_at.desc())
            .all()
        )

    # ============================================================
    # UPDATE
    # ============================================================

    def update_last_used(self, api_key: ApiKey):
        api_key.last_used_at = datetime.now(timezone.utc)

    def deactivate(self, api_key: ApiKey):
        api_key.is_active = False