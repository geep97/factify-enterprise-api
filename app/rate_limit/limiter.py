from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session

from app.db.models import Organization, UsageRecord
from app.rate_limit.service import RateLimitService


class RateLimiter:
    """Enterprise rate limiting."""

    @staticmethod
    def check(
        db: Session,
        organization: Organization,
    ) -> tuple[bool, int, int]:
        """
        Check whether an organization is allowed to make another request.

        Returns:
            (
                allowed,
                remaining_requests,
                requests_per_hour,
            )
        """

        rate_limit = RateLimitService.get_by_organization(
            db,
            organization.id,
        )

        if rate_limit is None:
            return True, 0, 0

        if not rate_limit.is_enabled:
            return True, 0, rate_limit.requests_per_hour

        window_start = (
            datetime.now(timezone.utc)
            - timedelta(hours=1)
        )

        requests_used = (
            db.query(UsageRecord)
            .filter(
                UsageRecord.organization_id == organization.id,
                UsageRecord.created_at >= window_start,
            )
            .count()
        )

        remaining = max(
            0,
            rate_limit.requests_per_hour - requests_used,
        )

        allowed = requests_used < rate_limit.requests_per_hour

        return (
            allowed,
            remaining,
            rate_limit.requests_per_hour,
        )

    @staticmethod
    def record_request(
        db: Session,
        organization: Organization,
        endpoint: str,
        status_code: int,
    ) -> UsageRecord:
        """
        Record a successful request.
        """

        usage = UsageRecord(
            organization_id=organization.id,
            endpoint=endpoint,
            status_code=status_code,
        )

        db.add(usage)
        db.commit()
        db.refresh(usage)

        return usage

    @staticmethod
    def get_status(
        db: Session,
        organization: Organization,
    ) -> dict:
        """
        Return the organization's current rate limit status.
        """

        rate_limit = RateLimitService.get_by_organization(
            db,
            organization.id,
        )

        if rate_limit is None:
            return {
                "organization": organization.name,
                "requests_used": 0,
                "requests_remaining": 0,
                "requests_per_hour": 0,
                "enabled": False,
            }

        window_start = (
            datetime.now(timezone.utc)
            - timedelta(hours=1)
        )

        requests_used = (
            db.query(UsageRecord)
            .filter(
                UsageRecord.organization_id == organization.id,
                UsageRecord.created_at >= window_start,
            )
            .count()
        )

        requests_remaining = max(
            0,
            rate_limit.requests_per_hour - requests_used,
        )

        return {
            "organization": organization.name,
            "requests_used": requests_used,
            "requests_remaining": requests_remaining,
            "requests_per_hour": rate_limit.requests_per_hour,
            "enabled": rate_limit.is_enabled,
        }