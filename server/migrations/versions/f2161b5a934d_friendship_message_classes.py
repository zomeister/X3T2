"""Friendship() & Message() classes

Revision ID: f2161b5a934d
Revises: 158b7bf2d306
Create Date: 2023-09-12 17:14:15.315762

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f2161b5a934d'
down_revision = '158b7bf2d306'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('messages',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('message', sa.String(), nullable=True),
    sa.Column('status', sa.String(), nullable=True),
    sa.Column('friendship_id', sa.Integer(), nullable=True),
    sa.Column('author_id', sa.Integer(), nullable=True),
    sa.Column('reader_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['author_id'], ['users.id'], name=op.f('fk_messages_author_id_users')),
    sa.ForeignKeyConstraint(['friendship_id'], ['friendships.id'], name=op.f('fk_messages_friendship_id_friendships')),
    sa.ForeignKeyConstraint(['reader_id'], ['users.id'], name=op.f('fk_messages_reader_id_users')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_messages'))
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('messages')
    # ### end Alembic commands ###
