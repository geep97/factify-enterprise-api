from datetime import datetime

from pydantic import BaseModel, ConfigDict


# ============================================================
# ORGANIZATION
# ============================================================

class DashboardOrganization(BaseModel):
    id: int
    name: str
    slug: str

    model_config = ConfigDict(from_attributes=True)


# ============================================================
# SUBSCRIPTION
# ============================================================

class DashboardSubscription(BaseModel):
    plan_name: str
    status: str
    monthly_request_limit: int
    pending_plan_name: str | None = None
    pending_plan_effective_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)


# ============================================================
# USAGE
# ============================================================

class DashboardUsage(BaseModel):
    requests_used: int
    requests_remaining: int


# ============================================================
# API KEYS
# ============================================================

class DashboardApiKeys(BaseModel):
    total: int
    active: int
    inactive: int


# ============================================================
# RATE LIMIT
# ============================================================

class DashboardRateLimit(BaseModel):
    requests_per_hour: int


# ============================================================
# RESPONSE
# ============================================================

class DashboardResponse(BaseModel):
    organization: DashboardOrganization
    subscription: DashboardSubscription
    usage: DashboardUsage
    api_keys: DashboardApiKeys
    rate_limit: DashboardRateLimit


# ============================================================
# USAGE SERIES (for charts)
# ============================================================

class DashboardUsagePoint(BaseModel):
    date: str
    count: int


class DashboardUsageSeriesResponse(BaseModel):
    api_key_id: int | None
    days: int
    points: list[DashboardUsagePoint]