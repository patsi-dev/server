"""Creating users table

Revision ID: 037dbec70205
Revises: ebc626e70d5e
Create Date: 2024-11-21 11:07:11.622293

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '037dbec70205'
down_revision = 'ebc626e70d5e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_name', sa.String(length=60), nullable=False),
    sa.Column('email', sa.String(length=60), nullable=False),
    sa.Column('password', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_users')),
    sa.UniqueConstraint('email', name=op.f('uq_users_email'))
    )
    with op.batch_alter_table('customers', schema=None) as batch_op:
        batch_op.alter_column('phone',
               existing_type=sa.VARCHAR(length=60),
               type_=sa.String(length=15),
               existing_nullable=False)
        batch_op.alter_column('email',
               existing_type=sa.VARCHAR(length=60),
               type_=sa.String(length=80),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('customers', schema=None) as batch_op:
        batch_op.alter_column('email',
               existing_type=sa.String(length=80),
               type_=sa.VARCHAR(length=60),
               existing_nullable=False)
        batch_op.alter_column('phone',
               existing_type=sa.String(length=15),
               type_=sa.VARCHAR(length=60),
               existing_nullable=False)

    op.drop_table('users')
    # ### end Alembic commands ###
