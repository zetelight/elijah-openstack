"""empty message

Revision ID: 2dffb08fef5f
Revises: 66d21032c506
Create Date: 2017-04-26 18:45:34.048037

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2dffb08fef5f'
down_revision = '66d21032c506'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('clusters', sa.Column('nameserver_port', sa.String(length=20), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('clusters', 'nameserver_port')
    # ### end Alembic commands ###
