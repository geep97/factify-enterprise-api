from sqlalchemy.orm import Session

from app.db.models import Organization, RateLimit


class RateLimitService:
    """Service for managing organization rate limits."""

    DEFAULT_REQUESTS_PER_HOUR = 1000

    @staticmethod
    def create_default(
        db: Session,
        organization: Organization,
    ) -> RateLimit:
        """
        Create a default rate limit for a new organization.
        """

        rate_limit = RateLimit(
            organization_id=organization.id,
            requests_per_hour=RateLimitService.DEFAULT_REQUESTS_PER_HOUR,
            is_enabled=True,
        )

        db.add(rate_limit)
        db.flush()

        return rate_limit

    @staticmethod
    def get_by_organization(
        db: Session,
        organization_id: int,
    ) -> RateLimit | None:
        """
        Retrieve an organization's rate limit.
        """

        return (
            db.query(RateLimit)
            .filter(RateLimit.organization_id == organization_id)
            .first()
        )

    @staticmethod
    def update_limit(
        db: Session,
        organization_id: int,
        requests_per_hour: int,
    ) -> RateLimit | None:
        """
        Update the requests-per-hour limit.
        """

        rate_limit = RateLimitService.get_by_organization(
            db,
            organization_id,
        )

        if rate_limit is None:
            return None

        rate_limit.requests_per_hour = requests_per_hour

        db.commit()
        db.refresh(rate_limit)

        return rate_limit

    @staticmethod
    def enable(
        db: Session,
        organization_id: int,
    ) -> RateLimit | None:
        """
        Enable rate limiting.
        """

        rate_limit = RateLimitService.get_by_organization(
            db,
            organization_id,
        )

        if rate_limit is None:
            return None

        rate_limit.is_enabled = True

        db.commit()
        db.refresh(rate_limit)

        return rate_limit

    @staticmethod
    def disable(
        db: Session,
        organization_id: int,
    ) -> RateLimit | None:
        """
        Disable rate limiting.
        """

        rate_limit = RateLimitService.get_by_organization(
            db,
            organization_id,
        )

        if rate_limit is None:
            return None

        rate_limit.is_enabled = False

        db.commit()
        db.refresh(rate_limit)

        return rate_limit

    @staticmethod
    def delete(
        db: Session,
        organization_id: int,
    ) -> bool:
        """
        Delete an organization's rate limit.
        """

        rate_limit = RateLimitService.get_by_organization(
            db,
            organization_id,
        )

        if rate_limit is None:
            return False

        db.delete(rate_limit)
        db.commit()

        return True