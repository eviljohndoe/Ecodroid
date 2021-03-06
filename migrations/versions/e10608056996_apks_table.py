"""apks table

Revision ID: e10608056996
Revises: dd4e694b3acf
Create Date: 2018-08-20 15:22:37.862657

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e10608056996'
down_revision = 'dd4e694b3acf'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('apk',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('package_name', sa.String(length=128), nullable=True),
    sa.Column('filename', sa.String(length=128), nullable=True),
    sa.Column('path', sa.String(length=256), nullable=True),
    sa.Column('version_code', sa.String(length=64), nullable=True),
    sa.Column('version_name', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_apk_package_name'), 'apk', ['package_name'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_apk_package_name'), table_name='apk')
    op.drop_table('apk')
    # ### end Alembic commands ###
