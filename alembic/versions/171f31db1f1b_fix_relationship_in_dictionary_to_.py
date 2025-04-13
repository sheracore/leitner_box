"""fix relationship in dictionary to dictionary examples

Revision ID: 171f31db1f1b
Revises: fea173073bbc
Create Date: 2025-04-12 15:18:15.416340

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '171f31db1f1b'
down_revision: Union[str, None] = 'fea173073bbc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
