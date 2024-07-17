"""create posts table

Revision ID: 25010b64d3a9
Revises: 
Create Date: 2024-07-15 08:46:13.513640

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '25010b64d3a9'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                    sa.Column('title', sa.String, nullable=False))
    pass


def downgrade():
    op.drop_table('posts')

    pass
