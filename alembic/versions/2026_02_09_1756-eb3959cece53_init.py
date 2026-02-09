"""Init

Revision ID: eb3959cece53
Revises:
Create Date: 2026-02-09 17:56:07.716766

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "eb3959cece53"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("telegram_id", sa.BigInteger(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("users_pkey")),
        sa.UniqueConstraint("telegram_id", name=op.f("users_telegram_id_key")),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("users")
