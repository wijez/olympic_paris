"""events_table

Revision ID: 8b2c971cbaa4
Revises: 1cfc2b1d5469
Create Date: 2024-08-09 16:44:31.870458

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.engine.reflection import Inspector

# revision identifiers, used by Alembic.
revision: str = '8b2c971cbaa4'
down_revision: Union[str, None] = '1cfc2b1d5469'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    bind = op.get_bind()
    inspector = Inspector.from_engine(bind)

    if 'events' not in inspector.get_table_names():
        op.create_table(
            'events',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('day', sa.DateTime(), nullable=False),
            sa.Column('name', sa.String(), nullable=True),
            sa.Column('venue_name', sa.String(), nullable=True),
            sa.Column('event_name', sa.String(), nullable=True),
            sa.Column('detailed_event_name', sa.String(), nullable=True),
            sa.Column('start_date', sa.DateTime(), nullable=True),
            sa.Column('end_date', sa.DateTime(), nullable=True),
            sa.Column('status', sa.String(), nullable=True),
            sa.Column('is_medal_event', sa.Boolean(), nullable=True),
            sa.Column('is_live', sa.Boolean(), nullable=True),
            sa.Column('gender_code', sa.String(), nullable=True),
            sa.Column('discipline_id', sa.String(), sa.ForeignKey("disciplines.id"), nullable=False),
            sa.Column('venue_id', sa.String(), sa.ForeignKey("venues.id"), nullable=False),
            sa.PrimaryKeyConstraint('id'),
            sa.Column('created_at', sa.DateTime, server_default=sa.func.now()),
            sa.Column('updated_at', sa.DateTime, onupdate=sa.func.now())
        )


def downgrade() -> None:
    bind = op.get_bind()
    inspector = Inspector.from_engine(bind)

    if 'events' in inspector.get_table_names():
        op.drop_table('events')
