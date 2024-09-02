"""competitor_table

Revision ID: d819fdf10eef
Revises: 8b2c971cbaa4
Create Date: 2024-08-09 16:44:36.095398

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.engine import reflection
from sqlalchemy.engine.reflection import Inspector

# revision identifiers, used by Alembic.
revision: str = 'd819fdf10eef'
down_revision: Union[str, None] = '8b2c971cbaa4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    bind = op.get_bind()
    inspector = reflection.Inspector.from_engine(bind)

    if 'competitors' not in inspector.get_table_names():
        op.create_table(
            'competitors',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('event_id', sa.Integer(), nullable=False),
            sa.Column('country_id', sa.String(), nullable=False),
            sa.Column('competitor_name', sa.String(), nullable=True),
            sa.Column('position', sa.Integer(), nullable=True),
            sa.Column('result_position', sa.String(), nullable=True),
            sa.Column('result_winnerLoserTie', sa.String(), nullable=True),
            sa.Column('result_mark', sa.Integer(), nullable=True),
            sa.PrimaryKeyConstraint('id'),
            sa.ForeignKeyConstraint(['event_id'], ['events.id'], ondelete='CASCADE'),
            sa.ForeignKeyConstraint(['country_id'], ['countries.id'], ondelete='SET NULL'),
            sa.Column('created_at', sa.DateTime, server_default=sa.func.now()),
            sa.Column('updated_at', sa.DateTime, onupdate=sa.func.now())
        )


def downgrade() -> None:
    bind = op.get_bind()
    inspector = reflection.Inspector.from_engine(bind)

    if 'competitors' in inspector.get_table_names():
        op.drop_table('competitors')
