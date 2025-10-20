"""Add new fields for User table

Revision ID: bc40a4972766
Revises: dc8a89ef41e3
Create Date: 2025-10-20 13:49:31.217104

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "bc40a4972766"
down_revision: Union[str, Sequence[str], None] = "dc8a89ef41e3"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "users", sa.Column("is_active", sa.Boolean(), nullable=False)
    )
    op.add_column(
        "users", sa.Column("is_verified", sa.Boolean(), nullable=False)
    )
    op.add_column(
        "users", sa.Column("is_superuser", sa.Boolean(), nullable=False)
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("users", "is_superuser")
    op.drop_column("users", "is_verified")
    op.drop_column("users", "is_active")
