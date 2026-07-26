from fastapi import APIRouter, Depends, HTTPException, Query

from app.auth.dependencies import get_current_user
from app.core.container import get_dashboard_service
from app.db.models.user import User
from app.schemas.dashboard import DashboardResponse, DashboardUsageSeriesResponse
from app.services.dashboard_service import DashboardService

router = APIRouter()


# ============================================================
# GET DASHBOARD
# ============================================================

@router.get("/", response_model=DashboardResponse)
def get_dashboard(
    user: User = Depends(get_current_user),
    service: DashboardService = Depends(get_dashboard_service),
):
    return service.get_dashboard(user.organization_id)


# ============================================================
# GET USAGE SERIES (for charts)
# ============================================================

@router.get("/usage-series", response_model=DashboardUsageSeriesResponse)
def get_usage_series(
    api_key_id: int | None = Query(default=None),
    days: int = Query(default=30, ge=1, le=90),
    user: User = Depends(get_current_user),
    service: DashboardService = Depends(get_dashboard_service),
):
    try:
        return service.get_usage_series(
            organization_id=user.organization_id,
            api_key_id=api_key_id,
            days=days,
        )

    except ValueError:
        raise HTTPException(
            status_code=404,
            detail="API key not found.",
        )