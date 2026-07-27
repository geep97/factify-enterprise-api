from fastapi import APIRouter, Depends

from app.auth.dependencies import get_current_api_key
from app.core.container import get_subscription_service
from app.db.models.api_key import ApiKey
from app.schemas.plans import PlanInfo
from app.schemas.subscription import SubscriptionResponse
from app.services.subscription_service import SubscriptionService
from app.subscriptions.plans import PLANS

router = APIRouter()


# ============================================================
# GET CURRENT SUBSCRIPTION
# ============================================================

@router.get("/", response_model=SubscriptionResponse)
def get_subscription(
    api_key: ApiKey = Depends(get_current_api_key),
    service: SubscriptionService = Depends(get_subscription_service),
):
    subscription = service.get_by_organization(
        api_key.organization_id
    )

    return SubscriptionResponse.model_validate(subscription)


# ============================================================
# CHECK SUBSCRIPTION STATUS
# ============================================================

@router.get("/status")
def subscription_status(
    api_key: ApiKey = Depends(get_current_api_key),
    service: SubscriptionService = Depends(get_subscription_service),
):
    service.is_active(api_key.organization_id)

    return {
        "active": True,
    }


# ============================================================
# LIST AVAILABLE PLANS (public — used by pricing/upgrade UI)
# ============================================================

@router.get("/plans", response_model=list[PlanInfo])
def list_plans():
    plans = []

    for plan in PLANS.values():
        if plan.price_pesewas is None:
            price_display = "Contact us"
        elif plan.price_pesewas == 0:
            price_display = "Free"
        else:
            price_display = f"GH\u20b5{plan.price_pesewas / 100:,.0f}/mo"

        plans.append(
            PlanInfo(
                name=plan.name,
                monthly_request_limit=plan.monthly_request_limit,
                requests_per_hour=plan.requests_per_hour,
                price_pesewas=plan.price_pesewas,
                price_display=price_display,
                self_serve=plan.is_self_serve,
            )
        )

    return plans