"""Added two columns in the employee section

Revision ID: 9e6ad7909d83
Revises: 037dbec70205
Create Date: 2024-12-04 14:33:02.027043

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9e6ad7909d83'
down_revision = '037dbec70205'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('employees', schema=None) as batch_op:
        batch_op.add_column(sa.Column('id_no', sa.String(length=60)))
        batch_op.add_column(sa.Column('contacts', sa.String(length=60)))
        batch_op.drop_constraint('uq_employees_contact_details', type_='unique')
        batch_op.create_unique_constraint(batch_op.f('uq_employees_contacts'), ['contacts'])
        batch_op.create_unique_constraint(batch_op.f('uq_employees_id_no'), ['id_no'])
        batch_op.drop_column('contact_details')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('employees', schema=None) as batch_op:
        batch_op.add_column(sa.Column('contact_details', sa.VARCHAR(length=60), nullable=False))
        batch_op.drop_constraint(batch_op.f('uq_employees_id_no'), type_='unique')
        batch_op.drop_constraint(batch_op.f('uq_employees_contacts'), type_='unique')
        batch_op.create_unique_constraint('uq_employees_contact_details', ['contact_details'])
        batch_op.drop_column('contacts')
        batch_op.drop_column('id_no')

    # ### end Alembic commands ###