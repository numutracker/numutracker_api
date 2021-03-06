"""add deleted_ tables to track deleted releases and artists

Revision ID: baee0a6588d1
Revises: 6c4a502736e7
Create Date: 2019-02-14 21:31:08.578572

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'baee0a6588d1'
down_revision = '6c4a502736e7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('deleted_artist',
    sa.Column('mbid', sa.String(length=36), nullable=False),
    sa.Column('date_deleted', sa.DateTime(timezone=True), nullable=False),
    sa.Column('meta', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('mbid')
    )
    op.create_table('deleted_release',
    sa.Column('mbid', sa.String(length=36), nullable=False),
    sa.Column('date_deleted', sa.DateTime(timezone=True), nullable=False),
    sa.Column('meta', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('mbid')
    )
    op.alter_column('artist', 'date_updated',
               existing_type=postgresql.TIMESTAMP(timezone=True),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('artist', 'date_updated',
               existing_type=postgresql.TIMESTAMP(timezone=True),
               nullable=True)
    op.drop_table('deleted_release')
    op.drop_table('deleted_artist')
    # ### end Alembic commands ###
