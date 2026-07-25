from app.core.security import (
    generate_api_key,
    get_key_prefix,
    hash_api_key,
    hash_password,
)
from app.db.models.api_key import ApiKey
from app.db.models.organization import Organization
from app.db.models.user import User
from app.rate_limit.service import RateLimitService
from app.services.subscription_service import SubscriptionService
from app.unit_of_work.unit_of_work import UnitOfWork


class RegistrationService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow
        self.subscription_service = SubscriptionService(uow)

    # ============================================================
    # REGISTER ORGANIZATION + USER + FIRST API KEY
    # ============================================================

    def register(
        self,
        organization_name: str,
        organization_slug: str,
        email: str,
        password: str,
        key_name: str = "Default API Key",
    ) -> tuple[Organization, User, str]:

        organization = Organization(
            name=organization_name,
            slug=organization_slug,
        )

        user = User(
            email=email,
            hashed_password=hash_password(password),
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

            # Attach user to the organization
            user.organization_id = organization.id
            self.uow.users.create(user)

            # Create the organization's first API key
            api_key = ApiKey(
                organization_id=organization.id,
                name=key_name,
                key_hash=hash_api_key(raw_api_key),
                key_prefix=get_key_prefix(raw_api_key),
            )

            self.uow.api_keys.create(api_key)

        # Refresh after commit
        self.uow.refresh(organization)
        self.uow.refresh(user)

        return organization, user, raw_api_key