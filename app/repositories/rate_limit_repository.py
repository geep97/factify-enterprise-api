from sqlalchemy.orm import Session

from app.db.models.rate_limit import RateLimit


class RateLimitRepository:
    def __init__(self, db: Session):
        self.db = db

    # ============================================================
    # CREATE
    # ============================================================

    def create(self, rate_limit: RateLimit):
        self.db.add(rate_limit)
        return rate_limit

    # ============================================================
    # READ
    # ============================================================

    def get_by_id(self, rate_limit_id: int):
        return (
            self.db.query(RateLimit)
            .filter(RateLimit.id == rate_limit_id)
            .first()
        )

    def get_by_organization_id(self, organization_id: int):
        return (
            self.db.query(RateLimit)
            .filter(RateLimit.organization_id == organization_id)
            .first()
        )

    # ============================================================
    # UPDATE
    # ============================================================

    def update_requests_per_hour(
        self,
        rate_limit: RateLimit,
        requests_per_hour: int,
    ):
        rate_limit.requests_per_hour = requests_per_hour

    def enable(self, rate_limit: RateLimit):
        rate_limit.is_enabled = True

    def disable(self, rate_limit: RateLimit):
        rate_limit.is_enabled = False

    # ============================================================
    # DELETE
    # ============================================================

    def delete(self, rate_limit: RateLimit):
        self.db.delete(rate_limit)