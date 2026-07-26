from datetime import datetime, timezone

from sqlalchemy import func
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
        api_key_id: int | None = None,
    ):
        usage = UsageRecord(
            organization_id=organization_id,
            endpoint=endpoint,
            status_code=status_code,
            api_key_id=api_key_id,
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

    def get_daily_usage(
        self,
        organization_id: int,
        since: datetime,
        api_key_id: int | None = None,
    ):
        """
        Returns (day, count) rows for the given organization,
        grouped by calendar day, from `since` onward. Days with
        zero requests are simply absent from the result — the
        caller fills gaps.
        """

        day_column = func.date_trunc("day", UsageRecord.created_at)

        query = self.db.query(
            day_column.label("day"),
            func.count(UsageRecord.id).label("count"),
        ).filter(
            UsageRecord.organization_id == organization_id,
            UsageRecord.created_at >= since,
        )

        if api_key_id is not None:
            query = query.filter(UsageRecord.api_key_id == api_key_id)

        return (
            query.group_by(day_column)
            .order_by(day_column)
            .all()
        )

    # ============================================================
    # UPDATE
    # ============================================================

    def update_last_used(self, api_key):
        api_key.last_used_at = datetime.now(timezone.utc)