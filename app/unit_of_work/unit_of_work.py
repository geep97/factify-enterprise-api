from sqlalchemy.orm import Session

from app.repositories.api_key_repository import ApiKeyRepository
from app.repositories.organization_repository import OrganizationRepository
from app.repositories.usage_repository import UsageRepository


class UnitOfWork:
    def __init__(self, db: Session):
        self.db = db

        self._api_keys = None
        self._organizations = None
        self._usage = None

    # ============================================================
    # REPOSITORIES
    # ============================================================

    @property
    def api_keys(self) -> ApiKeyRepository:
        if self._api_keys is None:
            self._api_keys = ApiKeyRepository(self.db)
        return self._api_keys

    @property
    def organizations(self) -> OrganizationRepository:
        if self._organizations is None:
            self._organizations = OrganizationRepository(self.db)
        return self._organizations

    @property
    def usage(self) -> UsageRepository:
        if self._usage is None:
            self._usage = UsageRepository(self.db)
        return self._usage

    # ============================================================
    # CONTEXT MANAGER
    # ============================================================

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.commit()
        else:
            self.rollback()

    # ============================================================
    # TRANSACTIONS
    # ============================================================

    def commit(self):
        self.db.commit()

    def rollback(self):
        self.db.rollback()

    def flush(self):
        self.db.flush()

    def refresh(self, entity):
        self.db.refresh(entity)