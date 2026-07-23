from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class ApiKey(Base):
    __tablename__ = "api_keys"

    id: Mapped[int] = mapped_column(primary_key=True)

    organization_id: Mapped[int] = mapped_column(
        ForeignKey("organizations.id"),
        nullable=False,
        index=True,
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    key_hash: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
    )

    key_prefix: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    last_used_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    organization = relationship(
        "Organization",
        back_populates="api_keys",
    )