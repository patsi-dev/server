"""Added unique constraints

Revision ID: 1af7ae0ef0d1
Revises: 1eb4a2b9fb32
Create Date: 2024-12-04 14:41:50.257329

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1af7ae0ef0d1'
down_revision = '1eb4a2b9fb32'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('employees', schema=None) as batch_op:
        batch_op.alter_column('id_no',
               existing_type=sa.VARCHAR(length=60),
               nullable=False)
        batch_op.alter_column('contacts',
               existing_type=sa.VARCHAR(length=60),
               nullable=False)
        batch_op.create_unique_constraint(batch_op.f('uq_employees_contacts'), ['contacts'])
        batch_op.create_unique_constraint(batch_op.f('uq_employees_id_no'), ['id_no'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('employees', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('uq_employees_id_no'), type_='unique')
        batch_op.drop_constraint(batch_op.f('uq_employees_contacts'), type_='unique')
        batch_op.alter_column('contacts',
               existing_type=sa.VARCHAR(length=60),
               nullable=True)
        batch_op.alter_column('id_no',
               existing_type=sa.VARCHAR(length=60),
               nullable=True)

    # ### end Alembic commands ###