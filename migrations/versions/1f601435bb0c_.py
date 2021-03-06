"""empty message

Revision ID: 1f601435bb0c
Revises: 44f00400f426
Create Date: 2021-09-20 12:52:34.269171

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '1f601435bb0c'
down_revision = '44f00400f426'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('order', sa.Column('destination', sa.Integer(), server_default=FetchedValue(), nullable=False))
    op.add_column('user', sa.Column('gravatar', sa.Integer(), nullable=True))
    op.alter_column('user', 'region',
               existing_type=mysql.VARCHAR(length=50),
               nullable=True)
    op.alter_column('user', 'signature',
               existing_type=mysql.VARCHAR(length=100),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'signature',
               existing_type=mysql.VARCHAR(length=100),
               nullable=False)
    op.alter_column('user', 'region',
               existing_type=mysql.VARCHAR(length=50),
               nullable=False)
    op.drop_column('user', 'gravatar')
    op.drop_column('order', 'destination')
    # ### end Alembic commands ###
