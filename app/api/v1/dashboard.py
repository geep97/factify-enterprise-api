from fastapi import APIRouter, Depends

from app.auth.dependencies import get_current_user
from app.core.container import get_dashboard_service
from app.db.models.user import User
from app.schemas.dashboard import DashboardResponse
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