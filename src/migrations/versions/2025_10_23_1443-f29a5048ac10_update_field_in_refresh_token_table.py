"""Update field in Refresh Token table

Revision ID: f29a5048ac10
Revises: 44b04af91f2c
Create Date: 2025-10-23 14:43:40.400736

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "f29a5048ac10"
down_revision: Union[str, Sequence[str], None] = "44b04af91f2c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column(
        "refresh_tokens",
        "token",
        existing_type=sa.VARCHAR(length=100),
        type_=sa.String(length=500),
        existing_nullable=False,
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column(
        "refresh_tokens",
        "token",
        existing_type=sa.String(length=500),
        type_=sa.VARCHAR(length=100),
        existing_nullable=False,
    )
