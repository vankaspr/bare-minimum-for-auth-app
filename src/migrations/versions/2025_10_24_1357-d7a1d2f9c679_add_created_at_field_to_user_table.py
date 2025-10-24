"""Add created_at field to User table

Revision ID: d7a1d2f9c679
Revises: f29a5048ac10
Create Date: 2025-10-24 13:57:23.582877

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "d7a1d2f9c679"
down_revision: Union[str, Sequence[str], None] = "f29a5048ac10"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "users",
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("users", "created_at")
