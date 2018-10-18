"""new many_to_many_relations

Revision ID: 788ff3bb1518
Revises: e10608056996
Create Date: 2018-08-21 08:46:13.861188

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '788ff3bb1518'
down_revision = 'e10608056996'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('projects_apks',
    sa.Column('apk_id', sa.Integer(), nullable=True),
    sa.Column('project_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['apk_id'], ['apk.id'], ),
    sa.ForeignKeyConstraint(['project_id'], ['project.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('projects_apks')
    # ### end Alembic commands ###
