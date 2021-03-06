"""empty message

Revision ID: 2833870330ef
Revises: dd80f3a92ea4
Create Date: 2020-05-26 19:06:33.363129

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '2833870330ef'
down_revision = 'dd80f3a92ea4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('task', 'artefacts')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('task', sa.Column('artefacts', postgresql.ARRAY(sa.VARCHAR(length=255)), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
