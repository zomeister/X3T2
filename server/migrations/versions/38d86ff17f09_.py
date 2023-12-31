"""empty message

Revision ID: 38d86ff17f09
Revises: f2161b5a934d
Create Date: 2023-09-12 20:23:43.288544

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '38d86ff17f09'
down_revision = 'f2161b5a934d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('menus',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('emoji', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_menus')),
    sa.UniqueConstraint('emoji', name=op.f('uq_menus_emoji')),
    sa.UniqueConstraint('name', name=op.f('uq_menus_name'))
    )
    op.create_table('posts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('status', sa.String(), nullable=True),
    sa.Column('content', sa.String(), nullable=True),
    sa.Column('author_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['author_id'], ['users.id'], name=op.f('fk_posts_author_id_users')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_posts'))
    )
    with op.batch_alter_table('actions', schema=None) as batch_op:
        batch_op.add_column(sa.Column('menu_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(batch_op.f('fk_actions_menu_id_menus'), 'menus', ['menu_id'], ['id'])

    with op.batch_alter_table('adoptions', schema=None) as batch_op:
        batch_op.drop_column('username')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('adoptions', schema=None) as batch_op:
        batch_op.add_column(sa.Column('username', sa.VARCHAR(), nullable=True))

    with op.batch_alter_table('actions', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('fk_actions_menu_id_menus'), type_='foreignkey')
        batch_op.drop_column('menu_id')

    op.drop_table('posts')
    op.drop_table('menus')
    # ### end Alembic commands ###
