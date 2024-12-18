"""empty message

Revision ID: 88d56d8bfffc
Revises: e5c6e0f3af42
Create Date: 2024-11-20 21:36:50.231844

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '88d56d8bfffc'
down_revision = 'e5c6e0f3af42'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('_alembic_tmp_employees')
    with op.batch_alter_table('employees', schema=None) as batch_op:
        batch_op.add_column(sa.Column('id_no', sa.String(length=60), nullable=False))
        batch_op.create_unique_constraint(batch_op.f('uq_employees_contact_details'), ['contact_details'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('employees', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('uq_employees_contact_details'), type_='unique')
        batch_op.drop_column('id_no')

    op.create_table('_alembic_tmp_employees',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('name', sa.VARCHAR(length=60), nullable=False),
    sa.Column('position', sa.VARCHAR(length=60), nullable=False),
    sa.Column('contact_details', sa.VARCHAR(length=60), nullable=False),
    sa.PrimaryKeyConstraint('id', name='pk_employees'),
    sa.UniqueConstraint('contact_details', name='uq_employees_contact_details')
    )
    # ### end Alembic commands ###
