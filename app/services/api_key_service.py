from app.core.security import (
    generate_api_key,
    get_key_prefix,
    hash_api_key,
)
from app.db.models.api_key import ApiKey
from app.db.models.organization import Organization
from app.rate_limit.service import RateLimitService
from app.services.subscription_service import SubscriptionService
from app.unit_of_work.unit_of_work import UnitOfWork


class ApiKeyService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow
        self.subscription_service = SubscriptionService(uow)

    # ============================================================
    # CREATE ORGANIZATION + FIRST API KEY
    # ============================================================

    def create_organization_with_api_key(
        self,
        organization_name: str,
        organization_slug: str,
        key_name: str = "Default API Key",
    ) -> tuple[Organization, str]:

        organization = Organization(
            name=organization_name,
            slug=organization_slug,
        )

        raw_api_key = generate_api_key()

        with self.uow:
            # Create organization
            self.uow.organizations.create(organization)

            # Flush so PostgreSQL generates organization.id
            self.uow.flush()

            # Create default subscription
            self.subscription_service.create_default(organization)

            # Create default rate limit
            RateLimitService.create_default(
                db=self.uow.db,
                organization=organization,
            )

            # Create first API key
            api_key = ApiKey(
                organization_id=organization.id,
                name=key_name,
                key_hash=hash_api_key(raw_api_key),
                key_prefix=get_key_prefix(raw_api_key),
            )

            self.uow.api_keys.create(api_key)

        # Refresh after commit
        self.uow.refresh(organization)

        return organization, raw_api_key

    # ============================================================
    # CREATE ADDITIONAL API KEY
    # ============================================================

    def create_additional_api_key(
        self,
        organization: Organization,
        key_name: str,
    ) -> str:

        raw_api_key = generate_api_key()

        api_key = ApiKey(
            organization_id=organization.id,
            name=key_name,
            key_hash=hash_api_key(raw_api_key),
            key_prefix=get_key_prefix(raw_api_key),
        )

        with self.uow:
            self.uow.api_keys.create(api_key)

        return raw_api_key

    # ============================================================
    # REVOKE API KEY
    # ============================================================

    def revoke_api_key(
        self,
        organization_id: int,
        key_id: int,
    ) -> ApiKey:
        """
        Deactivate an API key belonging to the given organization.

        Raises:
            ValueError: if the key doesn't exist or belongs to
                        a different organization.
        """

        with self.uow:
            api_key = self.uow.api_keys.get_by_id(key_id)

            if api_key is None or api_key.organization_id != organization_id:
                raise ValueError("API key not found.")

            self.uow.api_keys.deactivate(api_key)

        self.uow.refresh(api_key)

        return api_key

    # ============================================================
    # ROTATE API KEY
    # ============================================================

    def rotate_api_key(
        self,
        organization_id: int,
        key_id: int,
    ) -> tuple[ApiKey, ApiKey, str]:
        """
        Deactivate an existing API key and issue a replacement,
        in a single transaction.

        Raises:
            ValueError: if the key doesn't exist or belongs to
                        a different organization.

        Returns:
            (old_key, new_key, raw_new_api_key)
        """

        raw_api_key = generate_api_key()

        with self.uow:
            old_key = self.uow.api_keys.get_by_id(key_id)

            if old_key is None or old_key.organization_id != organization_id:
                raise ValueError("API key not found.")

            self.uow.api_keys.deactivate(old_key)

            new_key = ApiKey(
                organization_id=organization_id,
                name=old_key.name,
                key_hash=hash_api_key(raw_api_key),
                key_prefix=get_key_prefix(raw_api_key),
            )

            self.uow.api_keys.create(new_key)

        self.uow.refresh(old_key)
        self.uow.refresh(new_key)

        return old_key, new_key, raw_api_key