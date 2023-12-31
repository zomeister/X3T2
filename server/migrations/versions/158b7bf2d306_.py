"""empty message

Revision ID: 158b7bf2d306
Revises: 0dfe179ee26c
Create Date: 2023-09-12 00:55:25.245735

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '158b7bf2d306'
down_revision = '0dfe179ee26c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('friendships',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('req_user_id', sa.Integer(), nullable=True),
    sa.Column('rec_user_id', sa.Integer(), nullable=True),
    sa.Column('status', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['rec_user_id'], ['users.id'], name=op.f('fk_friendships_rec_user_id_users')),
    sa.ForeignKeyConstraint(['req_user_id'], ['users.id'], name=op.f('fk_friendships_req_user_id_users')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_friendships'))
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('friendships')
    # ### end Alembic commands ###
