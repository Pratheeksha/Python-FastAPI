"""add content column to posts table

Revision ID: 093cee1789b4
Revises: 25010b64d3a9
Create Date: 2024-07-15 08:54:38.540018

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '093cee1789b4'
down_revision: Union[str, None] = '25010b64d3a9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
