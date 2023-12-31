"""empty message

Revision ID: 2d5442eff5aa
Revises: 9363b4919ce1
Create Date: 2023-09-12 22:51:21.180952

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2d5442eff5aa'
down_revision = '9363b4919ce1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('threads', schema=None) as batch_op:
        batch_op.add_column(sa.Column('friendship_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(batch_op.f('fk_threads_friendship_id_friendships'), 'friendships', ['friendship_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('threads', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('fk_threads_friendship_id_friendships'), type_='foreignkey')
        batch_op.drop_column('friendship_id')

    # ### end Alembic commands ###
