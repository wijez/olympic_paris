"""venues_table

Revision ID: 1cfc2b1d5469
Revises: 
Create Date: 2024-08-09 16:44:23.866378

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.engine.reflection import Inspector

# revision identifiers, used by Alembic.
revision: str = '1cfc2b1d5469'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    bind = op.get_bind()
    inspector = Inspector.from_engine(bind)
    if 'venues' not in inspector.get_table_names():
        op.create_table(
            'venues',
            sa.Column('id', sa.String, nullable=False, primary_key=True),
            sa.Column('name', sa.String, nullable=False),
            sa.Column('url', sa.String),
        )


def downgrade():
    # Drop the table if it exists
    bind = op.get_bind()
    inspector = Inspector.from_engine(bind)
    if 'venues' in inspector.get_table_names():
        op.drop_table('venues')
