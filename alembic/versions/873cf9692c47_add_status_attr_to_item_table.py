"""Add status attr to Item table

Revision ID: 873cf9692c47
Revises: 52a363648e1d
Create Date: 2024-04-13 00:35:14.246708

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '873cf9692c47'
down_revision: Union[str, None] = '52a363648e1d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Добавляем тип itemstatus в базу данных
    op.execute("CREATE TYPE itemstatus AS ENUM ('REVIEW', 'ACTIVE', 'REMOVED')")

    # Добавляем столбец с типом Enum
    op.add_column('items', sa.Column('status', sa.Enum('REVIEW', 'ACTIVE', 'REMOVED', name='itemstatus'), nullable=True))

def downgrade() -> None:
    # Удаляем столбец
    op.drop_column('items', 'status')

    # Удаляем тип Enum из базы данных
    op.execute("DROP TYPE itemstatus")
