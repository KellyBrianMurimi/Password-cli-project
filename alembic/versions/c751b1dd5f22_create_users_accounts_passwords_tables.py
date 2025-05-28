"""Create users, accounts, passwords tables

Revision ID: c751b1dd5f22
Revises: 
Create Date: 2025-05-28 13:49:33.298095
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'c751b1dd5f22'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('username', sa.String(), nullable=False, unique=True),
        sa.Column('email', sa.String(), nullable=False, unique=True),
    )

    op.create_table(
        'accounts',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id')),
    )

    op.create_table(
        'passwords',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('encrypted_password', sa.String(), nullable=False),
        sa.Column('account_id', sa.Integer(), sa.ForeignKey('accounts.id')),
    )


def downgrade() -> None:
    op.drop_table('passwords')
    op.drop_table('accounts')
    op.drop_table('users')
