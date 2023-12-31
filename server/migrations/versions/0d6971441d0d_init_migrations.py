"""init migrations

Revision ID: 0d6971441d0d
Revises: 5a0670946776
Create Date: 2023-09-09 23:10:26.012395

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0d6971441d0d'
down_revision = '5a0670946776'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('actions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_actions'))
    )
    op.create_table('adoptions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_adoptions'))
    )
    op.create_table('owners',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_owners'))
    )
    op.create_table('pets',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_pets'))
    )
    op.create_table('stats',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_stats'))
    )
    op.create_table('strains',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_strains'))
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_users'))
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    op.drop_table('strains')
    op.drop_table('stats')
    op.drop_table('pets')
    op.drop_table('owners')
    op.drop_table('adoptions')
    op.drop_table('actions')
    # ### end Alembic commands ###
