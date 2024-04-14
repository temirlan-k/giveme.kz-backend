"""add bonus attr to Item table

Revision ID: 92b9d35775e6
Revises: 39d6974cfa02
Create Date: 2024-04-14 02:04:23.022886

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '92b9d35775e6'
down_revision: Union[str, None] = '39d6974cfa02'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('items', sa.Column('bonus', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('items', 'bonus')
    # ### end Alembic commands ###
