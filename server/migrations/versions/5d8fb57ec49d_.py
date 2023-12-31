"""empty message

Revision ID: 5d8fb57ec49d
Revises: 38d86ff17f09
Create Date: 2023-09-12 21:52:03.310642

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5d8fb57ec49d'
down_revision = '38d86ff17f09'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('messages', schema=None) as batch_op:
        batch_op.add_column(sa.Column('created_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True))
        batch_op.add_column(sa.Column('updated_at', sa.DateTime(), nullable=True))
        batch_op.drop_constraint('fk_messages_friendship_id_friendships', type_='foreignkey')
        batch_op.drop_constraint('fk_messages_reader_id_users', type_='foreignkey')
        batch_op.drop_constraint('fk_messages_author_id_users', type_='foreignkey')
        batch_op.drop_column('reader_id')
        batch_op.drop_column('friendship_id')
        batch_op.drop_column('author_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('messages', schema=None) as batch_op:
        batch_op.add_column(sa.Column('author_id', sa.INTEGER(), nullable=True))
        batch_op.add_column(sa.Column('friendship_id', sa.INTEGER(), nullable=True))
        batch_op.add_column(sa.Column('reader_id', sa.INTEGER(), nullable=True))
        batch_op.create_foreign_key('fk_messages_author_id_users', 'users', ['author_id'], ['id'])
        batch_op.create_foreign_key('fk_messages_reader_id_users', 'users', ['reader_id'], ['id'])
        batch_op.create_foreign_key('fk_messages_friendship_id_friendships', 'friendships', ['friendship_id'], ['id'])
        batch_op.drop_column('updated_at')
        batch_op.drop_column('created_at')

    # ### end Alembic commands ###
