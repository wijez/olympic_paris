"""countries_table

Revision ID: e58093454694
Revises: 1df2254d30c8
Create Date: 2024-08-20 09:13:37.827742

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'e58093454694'
down_revision: Union[str, None] =  None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'countries',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('continent', sa.String(), nullable=False),
        sa.Column('flag_url', sa.String(), nullable=True),
        sa.Column('gold_medals', sa.Integer(), nullable=False),
        sa.Column('silver_medals', sa.Integer(), nullable=False),
        sa.Column('bronze_medals', sa.Integer(), nullable=False),
        sa.Column('total_medals', sa.Integer(), nullable=False),
        sa.Column('rank', sa.Integer(), nullable=False),
        sa.Column('rank_total_medals', sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('countries')
