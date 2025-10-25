"""Add new field to User

Revision ID: 1bfb1d55251d
Revises: d7a1d2f9c679
Create Date: 2025-10-25 13:44:56.781530

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "1bfb1d55251d"
down_revision: Union[str, Sequence[str], None] = "d7a1d2f9c679"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("users", sa.Column("github_id", sa.Integer(), nullable=True))
    op.create_unique_constraint(None, "users", ["github_id"])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(None, "users", type_="unique")
    op.drop_column("users", "github_id")