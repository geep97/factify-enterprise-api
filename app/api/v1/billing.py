import hashlib
import hmac

from fastapi import APIRouter, Depends, HTTPException, Request

from app.auth.dependencies import get_current_user
from app.core.config import settings
from app.core.container import get_billing_service
from app.db.models.user import User
from app.schemas.billing import (
    CheckoutRequest,
    CheckoutResponse,
    CheckoutStatusResponse,
)
from app.services.billing_service import BillingService
from app.unit_of_work.dependencies import get_unit_of_work
from app.unit_of_work.unit_of_work import UnitOfWork

router = APIRouter()


# ============================================================
# CREATE CHECKOUT
# ============================================================

@router.post("/checkout", response_model=CheckoutResponse)
async def create_checkout(
    request: CheckoutRequest,
    user: User = Depends(get_current_user),
    service: BillingService = Depends(get_billing_service),
):
    try:
        result = await service.initiate_upgrade(
            organization_id=user.organization_id,
            user_email=user.email,
            plan_name=request.plan_name,
        )

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return CheckoutResponse(**result)


# ============================================================
# CHECK CHECKOUT STATUS
# ============================================================

@router.get("/status/{reference}", response_model=CheckoutStatusResponse)
def get_checkout_status(
    reference: str,
    user: User = Depends(get_current_user),
    uow: UnitOfWork = Depends(get_unit_of_work),
):
    transaction = uow.payment_transactions.get_by_reference(reference)

    if transaction is None or transaction.organization_id != user.organization_id:
        raise HTTPException(status_code=404, detail="Transaction not found.")

    return CheckoutStatusResponse(
        reference=transaction.reference,
        status=transaction.status,
        plan_name=transaction.plan_name,
    )


# ============================================================
# WEBHOOK (called by Paystack, not by users)
# ============================================================

@router.post("/webhook")
async def paystack_webhook(
    request: Request,
    service: BillingService = Depends(get_billing_service),
):
    raw_body = await request.body()
    signature = request.headers.get("x-paystack-signature")

    if signature is None:
        raise HTTPException(status_code=400, detail="Missing signature.")

    expected_signature = hmac.new(
        settings.PAYSTACK_SECRET_KEY.encode("utf-8"),
        raw_body,
        hashlib.sha512,
    ).hexdigest()

    if not hmac.compare_digest(expected_signature, signature):
        raise HTTPException(status_code=400, detail="Invalid signature.")

    payload = await request.json()

    service.handle_webhook_event(payload)

    return {"status": "ok"}