from app.schemas.dashboard import (
    DashboardApiKeys,
    DashboardOrganization,
    DashboardRateLimit,
    DashboardResponse,
    DashboardSubscription,
    DashboardUsage,
)
from app.unit_of_work.unit_of_work import UnitOfWork


class DashboardService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

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

        subscription = self.uow.subscriptions.get_by_organization_id(
            organization_id
        )

        if subscription is None:
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
            subscription=DashboardSubscription.model_validate(
                subscription
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
                requests_per_hour=rate_limit.requests_per_hour
            ),
        )