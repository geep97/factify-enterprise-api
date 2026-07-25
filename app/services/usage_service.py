from app.core.exceptions import MonthlyLimitExceededException
from app.db.models.api_key import ApiKey
from app.services.subscription_service import SubscriptionService
from app.unit_of_work.unit_of_work import UnitOfWork


class UsageService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow
        self.subscription_service = SubscriptionService(uow)

    # ============================================================
    # CHECK MONTHLY LIMIT
    # ============================================================

    def check_monthly_limit(
        self,
        api_key: ApiKey,
    ):
        request_count = self.uow.usage.get_monthly_usage_count(
            api_key.organization_id
        )

        subscription = self.subscription_service.get_by_organization(
            api_key.organization_id
        )

        if subscription is None:
            raise ValueError(
                f"No subscription found for organization {api_key.organization_id}"
            )

        if request_count >= subscription.monthly_request_limit:
            raise MonthlyLimitExceededException(
                limit=subscription.monthly_request_limit,
                used=request_count,
            )

    # ============================================================
    # RECORD REQUEST
    # ============================================================

    def record_request(
        self,
        api_key: ApiKey,
        endpoint: str,
        status_code: int,
    ):
        with self.uow:
            self.uow.usage.log_request(
                organization_id=api_key.organization_id,
                endpoint=endpoint,
                status_code=status_code,
            )

            self.uow.api_keys.update_last_used(api_key)