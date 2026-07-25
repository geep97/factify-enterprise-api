from fastapi import APIRouter, Depends

from app.auth.dependencies import get_current_api_key
from app.core.container import get_dashboard_service
from app.db.models.api_key import ApiKey
from app.schemas.dashboard import DashboardResponse
from app.services.dashboard_service import DashboardService

router = APIRouter()


# ============================================================
# GET DASHBOARD
# ============================================================

@router.get("/", response_model=DashboardResponse)
def get_dashboard(
    api_key: ApiKey = Depends(get_current_api_key),
    service: DashboardService = Depends(get_dashboard_service),
):
    return service.get_dashboard(api_key.organization_id)