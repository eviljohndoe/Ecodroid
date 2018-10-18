"""devices table

Revision ID: 265ed985de18
Revises: ca89ccf2b306
Create Date: 2018-07-30 11:19:14.842505

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '265ed985de18'
down_revision = 'ca89ccf2b306'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('device',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('adb_sn', sa.String(length=128), nullable=True),
    sa.Column('constructor', sa.String(length=64), nullable=True),
    sa.Column('model', sa.String(length=64), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('imei', sa.String(length=128), nullable=True),
    sa.Column('project_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['project_id'], ['project.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_device_adb_sn'), 'device', ['adb_sn'], unique=True)
    op.create_index(op.f('ix_device_imei'), 'device', ['imei'], unique=True)
    op.create_index(op.f('ix_device_timestamp'), 'device', ['timestamp'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_device_timestamp'), table_name='device')
    op.drop_index(op.f('ix_device_imei'), table_name='device')
    op.drop_index(op.f('ix_device_adb_sn'), table_name='device')
    op.drop_table('device')
    # ### end Alembic commands ###
