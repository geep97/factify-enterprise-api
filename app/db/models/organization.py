from datetime import datetime, timezone

from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class Organization(Base):
    __tablename__ = "organizations"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    slug: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    # ============================================================
    # RELATIONSHIPS
    # ============================================================

    api_keys = relationship(
        "ApiKey",
        back_populates="organization",
        cascade="all, delete-orphan",
    )

    usage_records = relationship(
        "UsageRecord",
        back_populates="organization",
        cascade="all, delete-orphan",
    )

    rate_limit = relationship(
        "RateLimit",
        back_populates="organization",
        uselist=False,
        cascade="all, delete-orphan",
    )

    subscription = relationship(
        "Subscription",
        back_populates="organization",
        uselist=False,
        cascade="all, delete-orphan",
    )