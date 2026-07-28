from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


# ============================================================
# BASE
# ============================================================

class SubscriptionBase(BaseModel):
    plan_name: str
    monthly_request_limit: int = Field(gt=0)
    status: str


# ============================================================
# RESPONSE
# ============================================================

class SubscriptionResponse(SubscriptionBase):
    id: int
    organization_id: int
    starts_at: datetime
    renews_at: datetime
    pending_plan_name: str | None = None
    pending_plan_effective_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)


# ============================================================
# REQUESTS
# ============================================================

class UpgradeSubscriptionRequest(BaseModel):
    plan_name: str


class DowngradeSubscriptionRequest(BaseModel):
    plan_name: str


class CancelPendingDowngradeRequest(BaseModel):
    pass


class RenewSubscriptionRequest(BaseModel):
    months: int = Field(default=1, ge=1)


class UpdateMonthlyLimitRequest(BaseModel):
    monthly_request_limit: int = Field(gt=0)


class ActivateSubscriptionRequest(BaseModel):
    pass


class CancelSubscriptionRequest(BaseModel):
    pass