import secrets
from datetime import datetime, timezone

from app.clients.paystack_client import PaystackClient
from app.core.config import settings
from app.db.models.payment_transaction import PaymentTransaction
from app.rate_limit.service import RateLimitService
from app.services.subscription_service import SubscriptionService
from app.subscriptions.plans import get_plan
from app.unit_of_work.unit_of_work import UnitOfWork


class BillingService:
    def __init__(self, uow: UnitOfWork, paystack_client: PaystackClient):
        self.uow = uow
        self.paystack_client = paystack_client
        self.subscription_service = SubscriptionService(uow)

    # ============================================================
    # INITIATE UPGRADE (checkout)
    # ============================================================

    async def initiate_upgrade(
        self,
        organization_id: int,
        user_email: str,
        plan_name: str,
    ) -> dict:

        plan = get_plan(plan_name)

        if not plan.is_self_serve:
            raise ValueError(
                f"{plan.name} is not available for self-serve purchase."
            )

        reference = f"factify_{secrets.token_hex(12)}"

        transaction = PaymentTransaction(
            organization_id=organization_id,
            plan_name=plan.name,
            reference=reference,
            amount_pesewas=plan.price_pesewas,
            currency="GHS",
            status="pending",
        )

        with self.uow:
            self.uow.payment_transactions.create(transaction)

        callback_url = f"{settings.FRONTEND_URL}/dashboard/subscription/callback"

        result = await self.paystack_client.initialize_transaction(
            email=user_email,
            amount_pesewas=plan.price_pesewas,
            reference=reference,
            callback_url=callback_url,
            currency="GHS",
            metadata={
                "organization_id": organization_id,
                "plan_name": plan.name,
            },
        )

        return {
            "authorization_url": result["data"]["authorization_url"],
            "reference": reference,
        }

    # ============================================================
    # HANDLE WEBHOOK EVENT
    # ============================================================

    def handle_webhook_event(self, payload: dict) -> None:
        """
        Process a verified Paystack webhook payload. Idempotent —
        safe to call multiple times for the same event (Paystack
        retries failed deliveries).
        """

        if payload.get("event") != "charge.success":
            return

        data = payload.get("data", {})
        reference = data.get("reference")

        if not reference:
            return

        transaction = self.uow.payment_transactions.get_by_reference(reference)

        if transaction is None:
            # Not a reference we issued — ignore.
            return

        if transaction.status == "success":
            # Already processed. No-op, protects against duplicate
            # webhook delivery double-upgrading the org.
            return

        paid_amount = data.get("amount")
        paystack_status = data.get("status")

        with self.uow:
            if paystack_status != "success" or paid_amount != transaction.amount_pesewas:
                transaction.status = "failed"
                return

            plan = get_plan(transaction.plan_name)

            self.subscription_service.upgrade_plan(
                organization_id=transaction.organization_id,
                plan_name=plan.name,
            )

            # RateLimitService.update_limit commits internally; since
            # it shares this same UnitOfWork's db session, that commit
            # also persists the subscription change above. The
            # context manager's own commit on exit is then a no-op
            # on an already-clean session.
            RateLimitService.update_limit(
                db=self.uow.db,
                organization_id=transaction.organization_id,
                requests_per_hour=plan.requests_per_hour,
            )

            transaction.status = "success"
            transaction.verified_at = datetime.now(timezone.utc)