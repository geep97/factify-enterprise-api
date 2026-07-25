from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models.organization import Organization
from app.rate_limit.dependencies import enforce_rate_limit
from app.rate_limit.limiter import RateLimiter

router = APIRouter(
    prefix="/protected",
    tags=["Protected"],
)


@router.get("/me")
def who_am_i(
    organization: Organization = Depends(enforce_rate_limit),
    db: Session = Depends(get_db),
):
    RateLimiter.record_request(
        db=db,
        organization=organization,
        endpoint="/protected/me",
        status_code=200,
    )

    return {
        "organization_id": organization.id,
        "organization_name": organization.name,
    }