"""disciplines_table

Revision ID: 1df2254d30c8
Revises: 9194c91dcc26
Create Date: 2024-08-19 23:41:21.328793

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1df2254d30c8'
down_revision: Union[str, None] = 'e58093454694'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'disciplines',
        sa.Column('id', sa.String(),primary_key=True, nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('pictogram_url', sa.String(), nullable=False),
        sa.Column('pictogram_url_dark', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime, onupdate=sa.func.now())
    )


def downgrade() -> None:
    op.drop_table('disciplines')
