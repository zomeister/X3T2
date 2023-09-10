"""models

Revision ID: b18b67e412be
Revises: 0d6971441d0d
Create Date: 2023-09-09 23:27:30.526488

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b18b67e412be'
down_revision = '0d6971441d0d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('actions', schema=None) as batch_op:
        batch_op.add_column(sa.Column('name', sa.String(), nullable=False))
        batch_op.add_column(sa.Column('image_url', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('adoption_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(batch_op.f('fk_actions_adoption_id_adoptions'), 'adoptions', ['adoption_id'], ['id'])

    with op.batch_alter_table('adoptions', schema=None) as batch_op:
        batch_op.add_column(sa.Column('username', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('owner_id', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('pet_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(batch_op.f('fk_adoptions_owner_id_owners'), 'owners', ['owner_id'], ['id'])
        batch_op.create_foreign_key(batch_op.f('fk_adoptions_pet_id_pets'), 'pets', ['pet_id'], ['id'])

    with op.batch_alter_table('owners', schema=None) as batch_op:
        batch_op.add_column(sa.Column('first_name', sa.String(), nullable=False))
        batch_op.add_column(sa.Column('last_name', sa.String(), nullable=False))
        batch_op.add_column(sa.Column('username', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('profile_url', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('city', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('bio', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('user_id', sa.Integer(), nullable=True))
        batch_op.create_unique_constraint(batch_op.f('uq_owners_username'), ['username'])
        batch_op.create_foreign_key(batch_op.f('fk_owners_user_id_users'), 'users', ['user_id'], ['id'])

    with op.batch_alter_table('pets', schema=None) as batch_op:
        batch_op.add_column(sa.Column('name', sa.String(), nullable=False))
        batch_op.add_column(sa.Column('factor', sa.Integer(), nullable=False))
        batch_op.add_column(sa.Column('strain_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(batch_op.f('fk_pets_strain_id_strains'), 'strains', ['strain_id'], ['id'])

    with op.batch_alter_table('stats', schema=None) as batch_op:
        batch_op.add_column(sa.Column('happiness', sa.Integer(), nullable=False))
        batch_op.add_column(sa.Column('health', sa.Integer(), nullable=False))
        batch_op.add_column(sa.Column('hunger', sa.Integer(), nullable=False))
        batch_op.add_column(sa.Column('pet_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(batch_op.f('fk_stats_pet_id_pets'), 'pets', ['pet_id'], ['id'])

    with op.batch_alter_table('strains', schema=None) as batch_op:
        batch_op.add_column(sa.Column('name', sa.String(), nullable=False))
        batch_op.add_column(sa.Column('emoji', sa.String(), nullable=False))
        batch_op.create_unique_constraint(batch_op.f('uq_strains_name'), ['name'])

    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('username', sa.String(), nullable=False))
        batch_op.add_column(sa.Column('email', sa.String(), nullable=False))
        batch_op.add_column(sa.Column('_password_hash', sa.String(), nullable=True))
        batch_op.create_unique_constraint(batch_op.f('uq_users_email'), ['email'])
        batch_op.create_unique_constraint(batch_op.f('uq_users_username'), ['username'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('uq_users_username'), type_='unique')
        batch_op.drop_constraint(batch_op.f('uq_users_email'), type_='unique')
        batch_op.drop_column('_password_hash')
        batch_op.drop_column('email')
        batch_op.drop_column('username')

    with op.batch_alter_table('strains', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('uq_strains_name'), type_='unique')
        batch_op.drop_column('emoji')
        batch_op.drop_column('name')

    with op.batch_alter_table('stats', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('fk_stats_pet_id_pets'), type_='foreignkey')
        batch_op.drop_column('pet_id')
        batch_op.drop_column('hunger')
        batch_op.drop_column('health')
        batch_op.drop_column('happiness')

    with op.batch_alter_table('pets', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('fk_pets_strain_id_strains'), type_='foreignkey')
        batch_op.drop_column('strain_id')
        batch_op.drop_column('factor')
        batch_op.drop_column('name')

    with op.batch_alter_table('owners', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('fk_owners_user_id_users'), type_='foreignkey')
        batch_op.drop_constraint(batch_op.f('uq_owners_username'), type_='unique')
        batch_op.drop_column('user_id')
        batch_op.drop_column('bio')
        batch_op.drop_column('city')
        batch_op.drop_column('profile_url')
        batch_op.drop_column('username')
        batch_op.drop_column('last_name')
        batch_op.drop_column('first_name')

    with op.batch_alter_table('adoptions', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('fk_adoptions_pet_id_pets'), type_='foreignkey')
        batch_op.drop_constraint(batch_op.f('fk_adoptions_owner_id_owners'), type_='foreignkey')
        batch_op.drop_column('pet_id')
        batch_op.drop_column('owner_id')
        batch_op.drop_column('username')

    with op.batch_alter_table('actions', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('fk_actions_adoption_id_adoptions'), type_='foreignkey')
        batch_op.drop_column('adoption_id')
        batch_op.drop_column('image_url')
        batch_op.drop_column('name')

    # ### end Alembic commands ###
