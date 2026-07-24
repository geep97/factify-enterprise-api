from fastapi import APIRouter, Depends

from app.auth.dependencies import get_current_organization
from app.db.models.organization import Organization

router = APIRouter(
    prefix="/protected",
    tags=["Protected"],
)


@router.get("/me")
def who_am_i(
    organization: Organization = Depends(get_current_organization),
):
    return {
        "organization_id": organization.id,
        "organization_name": organization.name,
    }