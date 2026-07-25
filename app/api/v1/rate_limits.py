from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models.organization import Organization
from app.rate_limit.dependencies import enforce_rate_limit
from app.rate_limit.limiter import RateLimiter

router = APIRouter(
    prefix="/rate-limits",
    tags=["Rate Limits"],
)


@router.get("/me")
def my_rate_limit(
    organization: Organization = Depends(enforce_rate_limit),
    db: Session = Depends(get_db),
):
    return RateLimiter.get_status(
        db=db,
        organization=organization,
    )