"""add order status to Order table

Revision ID: d569fd5f263e
Revises: 89521d5b46d3
Create Date: 2024-04-23 17:41:35.368224

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd569fd5f263e'
down_revision: Union[str, None] = '89521d5b46d3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute("CREATE TYPE orderstatus AS ENUM ('PENDING', 'IN_DELIVERY', 'COMPLETED')")
    op.add_column('orders', sa.Column('status', sa.Enum('PENDING', 'IN_DELIVERY', 'COMPLETED', name='orderstatus'), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('orders', 'status')
    # ### end Alembic commands ###
