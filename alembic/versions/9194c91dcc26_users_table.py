"""users_table

Revision ID: 9194c91dcc26
Revises: d819fdf10eef
Create Date: 2024-08-15 14:38:59.860401

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from app.utils import RoleEnum

# revision identifiers, used by Alembic.
revision: str = '9194c91dcc26'
down_revision: Union[str, None] = 'd819fdf10eef'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', sa.UUID(), primary_key=True, nullable=False),
        sa.Column('username', sa.String(), nullable=False, index=True),
        sa.Column('email', sa.String(), nullable=False, index=True),
        sa.Column('hashed_password', sa.String(), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('role', sa.Enum(RoleEnum), default=RoleEnum.USER, nullable=False),
        sa.Column('verify_code', sa.String(), nullable=True),

    )
    op.execute("DO $$ BEGIN IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'roleenum') THEN CREATE TYPE roleenum AS ENUM ('SUPERUSER', 'ADMIN', 'USER'); END IF; END $$;")

    op.add_column("users", sa.Column('created_at', sa.DateTime, server_default=sa.func.now()))
    op.add_column("users", sa.Column('updated_at', sa.DateTime, onupdate=sa.func.now()))


def downgrade() -> None:
    op.execute("DROP TYPE IF EXISTS roleenum;")
    op.drop_table('users')
