from sqlalchemy.orm import Session

from app.repositories.api_key_repository import ApiKeyRepository
from app.repositories.organization_repository import OrganizationRepository
from app.repositories.payment_transaction_repository import PaymentTransactionRepository
from app.repositories.rate_limit_repository import RateLimitRepository
from app.repositories.subscription_repository import SubscriptionRepository
from app.repositories.usage_repository import UsageRepository
from app.repositories.user_repository import UserRepository


class UnitOfWork:
    def __init__(self, db: Session):
        self.db = db

        self._api_keys = None
        self._organizations = None
        self._subscriptions = None
        self._usage = None
        self._rate_limits = None
        self._users = None
        self._payment_transactions = None

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
    def subscriptions(self) -> SubscriptionRepository:
        if self._subscriptions is None:
            self._subscriptions = SubscriptionRepository(self.db)
        return self._subscriptions

    @property
    def usage(self) -> UsageRepository:
        if self._usage is None:
            self._usage = UsageRepository(self.db)
        return self._usage

    @property
    def rate_limits(self) -> RateLimitRepository:
        if self._rate_limits is None:
            self._rate_limits = RateLimitRepository(self.db)
        return self._rate_limits

    @property
    def users(self) -> UserRepository:
        if self._users is None:
            self._users = UserRepository(self.db)
        return self._users

    @property
    def payment_transactions(self) -> PaymentTransactionRepository:
        if self._payment_transactions is None:
            self._payment_transactions = PaymentTransactionRepository(self.db)
        return self._payment_transactions

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