from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.db.models.usage import UsageRecord


class UsageRepository:
    def __init__(self, db: Session):
        self.db = db

    # ============================================================
    # CREATE
    # ============================================================

    def log_request(
        self,
        organization_id: int,
        endpoint: str,
        status_code: int,
    ):
        usage = UsageRecord(
            organization_id=organization_id,
            endpoint=endpoint,
            status_code=status_code,
        )

        self.db.add(usage)

        return usage

    # ============================================================
    # READ
    # ============================================================

    def get_monthly_usage_count(
        self,
        organization_id: int,
    ):
        now = datetime.now(timezone.utc)

        start_of_month = datetime(
            now.year,
            now.month,
            1,
            tzinfo=timezone.utc,
        )

        return (
            self.db.query(UsageRecord)
            .filter(
                UsageRecord.organization_id == organization_id,
                UsageRecord.created_at >= start_of_month,
            )
            .count()
        )

    def get_usage_records(
        self,
        organization_id: int,
    ):
        return (
            self.db.query(UsageRecord)
            .filter(
                UsageRecord.organization_id == organization_id,
            )
            .order_by(UsageRecord.created_at.desc())
            .all()
        )

    # ============================================================
    # UPDATE
    # ============================================================

    def update_last_used(self, api_key):
        api_key.last_used_at = datetime.now(timezone.utc)