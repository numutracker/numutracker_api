"""add some indexes

Revision ID: f115cda1ba1c
Revises: bf9ea959d63b
Create Date: 2018-12-23 22:02:45.906165

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f115cda1ba1c'
down_revision = 'bf9ea959d63b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index(op.f('ix_artist_release_artist_mbid'), 'artist_release', ['artist_mbid'], unique=False)
    op.create_index(op.f('ix_artist_release_release_mbid'), 'artist_release', ['release_mbid'], unique=False)
    op.create_index('user_releases_listened', 'user_release', ['user_id', 'type', 'listened', sa.text('date_release DESC')], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('user_releases_listened', table_name='user_release')
    op.drop_index(op.f('ix_artist_release_release_mbid'), table_name='artist_release')
    op.drop_index(op.f('ix_artist_release_artist_mbid'), table_name='artist_release')
    # ### end Alembic commands ###
