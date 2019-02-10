"""create lock table

Revision ID: f7fa96222aa4
Revises: aa01d71095c6
Create Date: 2019-02-08 22:47:31.659693

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f7fa96222aa4'
down_revision = 'aa01d71095c6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('lock',
    sa.Column('process_name', sa.String(length=36), nullable=False),
    sa.Column('lock_acquired', sa.Boolean(), nullable=True),
    sa.Column('date_acquired', sa.DateTime(timezone=True), nullable=True),
    sa.PrimaryKeyConstraint('process_name')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('lock')
    # ### end Alembic commands ###