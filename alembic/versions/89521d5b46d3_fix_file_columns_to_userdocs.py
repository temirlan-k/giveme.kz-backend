from alembic import op
import sqlalchemy as sa
from sqlalchemy.engine.reflection import Inspector

revision = '89521d5b46d3'
down_revision = '1a3ab2eccd16'
branch_labels = None
depends_on = None

def upgrade():
    conn = op.get_bind()
    inspector = Inspector.from_engine(conn)
    columns = {column['name'] for column in inspector.get_columns('needer_files')}

    if 'electronic_id' not in columns:
        op.add_column('needer_files', sa.Column('electronic_id', sa.String(length=255), nullable=False))
    if 'benefit_document' not in columns:
        op.add_column('needer_files', sa.Column('benefit_document', sa.String(length=255), nullable=False))
    if 'user_photo' not in columns:
        op.add_column('needer_files', sa.Column('user_photo', sa.String(length=255), nullable=False))
    if 'needer_file' in columns:
        op.drop_column('needer_files', 'needer_file')

def downgrade():
    conn = op.get_bind()
    inspector = Inspector.from_engine(conn)
    columns = {column['name'] for column in inspector.get_columns('needer_files')}

    if 'needer_file' not in columns:
        op.add_column('needer_files', sa.Column('needer_file', sa.VARCHAR(length=255), nullable=False))
    if 'user_photo' in columns:
        op.drop_column('needer_files', 'user_photo')
    if 'benefit_document' in columns:
        op.drop_column('needer_files', 'benefit_document')
    if 'electronic_id' in columns:
        op.drop_column('needer_files', 'electronic_id')
