"""initial schema

Revision ID: ed3eea979b62
Revises:
Create Date: 2026-07-24 11:13:35.127404

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "ed3eea979b62"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    # Create rate_limits table
    op.create_table(
        "rate_limits",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("organization_id", sa.Integer(), nullable=False),
        sa.Column("requests_per_hour", sa.Integer(), nullable=False),
        sa.Column("is_enabled", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(
            ["organization_id"],
            ["organizations.id"],
            ondelete="CASCADE",
        ),
        sa.UniqueConstraint(
            "organization_id",
            name="uq_rate_limits_organization_id",
        ),
    )

    # Remove the old organization limit column
    op.drop_column(
        "organizations",
        "monthly_request_limit",
    )


def downgrade() -> None:
    """Downgrade schema."""

    # Restore old column
    op.add_column(
        "organizations",
        sa.Column(
            "monthly_request_limit",
            sa.Integer(),
            nullable=False,
            server_default="1000",
        ),
    )

    # Remove rate_limits table
    op.drop_table("rate_limits")