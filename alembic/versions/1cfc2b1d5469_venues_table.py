"""venues_table

Revision ID: 1cfc2b1d5469
Revises: 
Create Date: 2024-08-09 16:44:23.866378

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1cfc2b1d5469'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'venues',
        sa.Column('id', sa.String, primary_key=True, index=True),
        sa.Column('name', sa.String, nullable=False, index=True),
        sa.Column('url', sa.String),
    )


def downgrade() -> None:
    op.drop_table('venues')
