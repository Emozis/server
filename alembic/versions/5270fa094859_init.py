"""init

Revision ID: 5270fa094859
Revises: 
Create Date: 2025-01-06 22:20:45.504093

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5270fa094859'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('chat_logs', sa.Column('model_name', sa.String(length=255), nullable=True))


def downgrade() -> None:
    op.drop_column('chat_logs', 'model_name')