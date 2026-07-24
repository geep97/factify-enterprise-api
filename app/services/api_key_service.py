from app.core.security import (
    generate_api_key,
    get_key_prefix,
    hash_api_key,
)
from app.db.models.api_key import ApiKey
from app.db.models.organization import Organization
from app.rate_limit.service import RateLimitService
from app.unit_of_work.unit_of_work import UnitOfWork


class ApiKeyService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

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

            # Create default rate limit for the organization
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