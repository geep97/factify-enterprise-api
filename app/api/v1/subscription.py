from fastapi import APIRouter, Depends

from app.auth.dependencies import get_current_api_key
from app.core.container import get_subscription_service
from app.db.models.api_key import ApiKey
from app.schemas.subscription import SubscriptionResponse
from app.services.subscription_service import SubscriptionService

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