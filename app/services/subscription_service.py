from datetime import datetime, timedelta, timezone

from app.core.exceptions import (
    InactiveSubscriptionException,
    SubscriptionAlreadyActiveException,
    SubscriptionAlreadyCancelledException,
    SubscriptionNotFoundException,
)
from app.db.models.organization import Organization
from app.db.models.subscription import Subscription
from app.rate_limit.service import RateLimitService
from app.subscriptions.plans import FREE, get_plan
from app.unit_of_work.unit_of_work import UnitOfWork


class SubscriptionService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    # ============================================================
    # CREATE
    # ============================================================

    def create_default(
        self,
        organization: Organization,
    ) -> Subscription:

        subscription = Subscription(
            organization_id=organization.id,
            plan_name=FREE.name,
            monthly_request_limit=FREE.monthly_request_limit,
            status="active",
            starts_at=datetime.now(timezone.utc),
            renews_at=datetime.now(timezone.utc) + timedelta(days=30),
        )

        self.uow.subscriptions.create(subscription)

        return subscription

    # ============================================================
    # READ
    # ============================================================

    def get_by_organization(
        self,
        organization_id: int,
    ) -> Subscription:

        subscription = self.uow.subscriptions.get_by_organization_id(
            organization_id
        )

        if subscription is None:
            raise SubscriptionNotFoundException()

        self._apply_pending_downgrade_if_due(subscription)

        return subscription

    # ============================================================
    # UPDATE
    # ============================================================

    def upgrade_plan(
        self,
        organization_id: int,
        plan_name: str,
    ) -> Subscription:

        subscription = self.get_by_organization(
            organization_id
        )

        plan = get_plan(plan_name)

        subscription.plan_name = plan.name
        subscription.monthly_request_limit = (
            plan.monthly_request_limit
        )
        subscription.status = "active"

        # An upgrade always supersedes any scheduled downgrade.
        subscription.pending_plan_name = None
        subscription.pending_plan_effective_at = None

        return subscription

    def schedule_downgrade(
        self,
        organization_id: int,
        plan_name: str,
    ) -> Subscription:
        """
        Schedules a plan downgrade to take effect at the end of the
        current billing period (subscription.renews_at). No payment
        involved — moving to a cheaper plan is always free. The
        current plan's benefits continue uninterrupted until then.
        """

        subscription = self.get_by_organization(
            organization_id
        )

        plan = get_plan(plan_name)

        if plan.monthly_request_limit >= subscription.monthly_request_limit:
            raise ValueError(
                f"{plan.name} is not a downgrade from "
                f"{subscription.plan_name}."
            )

        subscription.pending_plan_name = plan.name
        subscription.pending_plan_effective_at = subscription.renews_at

        return subscription

    def cancel_pending_downgrade(
        self,
        organization_id: int,
    ) -> Subscription:

        subscription = self.get_by_organization(
            organization_id
        )

        if subscription.pending_plan_name is None:
            raise ValueError("No pending downgrade to cancel.")

        subscription.pending_plan_name = None
        subscription.pending_plan_effective_at = None

        return subscription

    def renew(
        self,
        organization_id: int,
        months: int = 1,
    ) -> Subscription:

        subscription = self.get_by_organization(
            organization_id
        )

        now = datetime.now(timezone.utc)

        subscription.starts_at = now
        subscription.renews_at = (
            now + timedelta(days=30 * months)
        )
        subscription.status = "active"

        return subscription

    def cancel(
        self,
        organization_id: int,
    ) -> Subscription:

        subscription = self.get_by_organization(
            organization_id
        )

        if subscription.status == "cancelled":
            raise SubscriptionAlreadyCancelledException()

        subscription.status = "cancelled"

        return subscription

    def activate(
        self,
        organization_id: int,
    ) -> Subscription:

        subscription = self.get_by_organization(
            organization_id
        )

        if subscription.status == "active":
            raise SubscriptionAlreadyActiveException()

        subscription.status = "active"

        return subscription

    def update_monthly_limit(
        self,
        organization_id: int,
        monthly_request_limit: int,
    ) -> Subscription:

        subscription = self.get_by_organization(
            organization_id
        )

        subscription.monthly_request_limit = (
            monthly_request_limit
        )

        return subscription

    # ============================================================
    # HELPERS
    # ============================================================

    def is_active(
        self,
        organization_id: int,
    ) -> bool:

        subscription = self.get_by_organization(
            organization_id
        )

        if subscription.status != "active":
            raise InactiveSubscriptionException()

        if subscription.renews_at <= datetime.now(
            timezone.utc
        ):
            raise InactiveSubscriptionException()

        return True

    def _apply_pending_downgrade_if_due(
        self,
        subscription: Subscription,
    ) -> None:
        """
        If a downgrade is scheduled and its effective time has
        passed, apply it now: switch the plan, monthly limit, and
        rate limit together, then clear the pending fields. Called
        automatically by get_by_organization, so any code path that
        reads a subscription naturally applies due downgrades —
        no scheduler or background job required.
        """

        if subscription.pending_plan_name is None:
            return

        if subscription.pending_plan_effective_at is None:
            return

        if datetime.now(timezone.utc) < subscription.pending_plan_effective_at:
            return

        plan = get_plan(subscription.pending_plan_name)

        subscription.plan_name = plan.name
        subscription.monthly_request_limit = plan.monthly_request_limit
        subscription.pending_plan_name = None
        subscription.pending_plan_effective_at = None

        # Shares this same UnitOfWork's db session, so its internal
        # commit also persists the subscription changes above.
        RateLimitService.update_limit(
            db=self.uow.db,
            organization_id=subscription.organization_id,
            requests_per_hour=plan.requests_per_hour,
        )