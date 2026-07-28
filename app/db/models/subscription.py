from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class Subscription(Base):
    __tablename__ = "subscriptions"

    id: Mapped[int] = mapped_column(primary_key=True)

    organization_id: Mapped[int] = mapped_column(
        ForeignKey("organizations.id"),
        unique=True,
        nullable=False,
    )

    plan_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        default="Free",
    )

    monthly_request_limit: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=5000,
    )

    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="active",
    )

    starts_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    renews_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    # A scheduled downgrade, applied lazily once
    # pending_plan_effective_at has passed. Both null
    # when no downgrade is pending.
    pending_plan_name: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    pending_plan_effective_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    organization = relationship(
        "Organization",
        back_populates="subscription",
    )