from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_organization
from app.db.database import get_db
from app.db.models import Organization
from app.rate_limit.limiter import RateLimiter


def enforce_rate_limit(
    organization: Organization = Depends(get_current_organization),
    db: Session = Depends(get_db),
) -> Organization:
    """
    Ensure the organization has not exceeded its rate limit.
    """

    allowed, remaining, limit = RateLimiter.check(
        db=db,
        organization=organization,
    )

    if not allowed:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded.",
            headers={
                "X-RateLimit-Limit": str(limit),
                "X-RateLimit-Remaining": "0",
            },
        )

    return organization