"""add dictionary examples model

Revision ID: fea173073bbc
Revises: 622d6d2784b9
Create Date: 2025-04-12 15:16:39.373678

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fea173073bbc'
down_revision: Union[str, None] = '622d6d2784b9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
