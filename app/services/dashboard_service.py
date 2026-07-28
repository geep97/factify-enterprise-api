from datetime import datetime, timedelta, timezone

from app.core.exceptions import SubscriptionNotFoundException
from app.schemas.dashboard import (
    DashboardApiKeys,
    DashboardOrganization,
    DashboardRateLimit,
    DashboardResponse,
    DashboardSubscription,
    DashboardUsage,
    DashboardUsagePoint,
    DashboardUsageSeriesResponse,
)
from app.services.subscription_service import SubscriptionService
from app.unit_of_work.unit_of_work import UnitOfWork


class DashboardService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow
        self.subscription_service = SubscriptionService(uow)

    # ============================================================
    # GET DASHBOARD
    # ============================================================

    def get_dashboard(
        self,
        organization_id: int,
    ) -> DashboardResponse:

        organization = self.uow.organizations.get_by_id(
            organization_id
        )

        if organization is None:
            raise ValueError("Organization not found.")

        try:
            subscription = self.subscription_service.get_by_organization(
                organization_id
            )
        except SubscriptionNotFoundException:
            raise ValueError("Subscription not found.")

        requests_used = self.uow.usage.get_monthly_usage_count(
            organization_id
        )

        api_keys = self.uow.api_keys.list_by_organization(
            organization_id
        )

        rate_limit = self.uow.rate_limits.get_by_organization_id(
            organization_id
        )

        if rate_limit is None:
            raise ValueError("Rate limit configuration not found.")

        monthly_limit = subscription.monthly_request_limit

        active_keys = sum(
            1 for key in api_keys if key.is_active
        )

        inactive_keys = len(api_keys) - active_keys

        return DashboardResponse(
            organization=DashboardOrganization.model_validate(
                organization
            ),
            subscription=DashboardSubscription(
                plan_name=subscription.plan_name,
                status=subscription.status,
                monthly_request_limit=subscription.monthly_request_limit,
                pending_plan_name=subscription.pending_plan_name,
                pending_plan_effective_at=subscription.pending_plan_effective_at,
            ),
            usage=DashboardUsage(
                requests_used=requests_used,
                requests_remaining=max(
                    monthly_limit - requests_used,
                    0,
                ),
            ),
            api_keys=DashboardApiKeys(
                total=len(api_keys),
                active=active_keys,
                inactive=inactive_keys,
            ),
            rate_limit=DashboardRateLimit(
                # rate_limit row is refreshed by the lazy-apply check
                # above when a downgrade just took effect, but the
                # object we already loaded here may be stale in that
                # exact instant — re-read it directly to be safe.
                requests_per_hour=self.uow.rate_limits.get_by_organization_id(
                    organization_id
                ).requests_per_hour
            ),
        )

    # ============================================================
    # GET USAGE SERIES (for charts)
    # ============================================================

    def get_usage_series(
        self,
        organization_id: int,
        api_key_id: int | None = None,
        days: int = 30,
    ) -> DashboardUsageSeriesResponse:
        """
        Daily request counts for the last `days` days, optionally
        scoped to a single API key.

        Raises:
            ValueError: if api_key_id is given but doesn't exist
                        or belongs to a different organization.
        """

        if api_key_id is not None:
            api_key = self.uow.api_keys.get_by_id(api_key_id)

            if api_key is None or api_key.organization_id != organization_id:
                raise ValueError("API key not found.")

        now = datetime.now(timezone.utc)
        start_day = (now - timedelta(days=days - 1)).date()
        since = datetime(
            start_day.year,
            start_day.month,
            start_day.day,
            tzinfo=timezone.utc,
        )

        rows = self.uow.usage.get_daily_usage(
            organization_id=organization_id,
            since=since,
            api_key_id=api_key_id,
        )

        counts_by_date = {row.day.date(): row.count for row in rows}

        points = [
            DashboardUsagePoint(
                date=(start_day + timedelta(days=offset)).isoformat(),
                count=counts_by_date.get(
                    start_day + timedelta(days=offset), 0
                ),
            )
            for offset in range(days)
        ]

        return DashboardUsageSeriesResponse(
            api_key_id=api_key_id,
            days=days,
            points=points,
        )