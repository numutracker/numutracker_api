"""add user_releases index

Revision ID: e11a57c718d0
Revises: ed89f8244911
Create Date: 2018-12-17 19:12:35.989320

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e11a57c718d0'
down_revision = 'ed89f8244911'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index('user_releases', 'user_release', ['user_id', 'type', sa.text('date_release DESC')], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('user_releases', table_name='user_release')
    # ### end Alembic commands ###
