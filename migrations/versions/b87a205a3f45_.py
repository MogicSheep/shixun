"""empty message

Revision ID: b87a205a3f45
Revises: 
Create Date: 2021-08-31 16:09:29.020519

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b87a205a3f45'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('address', sa.Column('isdefault', sa.Integer(), nullable=True))
    op.add_column('address', sa.Column('name', sa.String(length=50, collation='utf8_general_ci'), nullable=False))
    op.add_column('address', sa.Column('phone', sa.String(length=15), nullable=False))
    op.add_column('address', sa.Column('tags', sa.String(length=100), nullable=True))
    op.drop_table_comment(
        'address',
        existing_comment='地址',
        schema=None
    )
    op.drop_table_comment(
        'comment',
        existing_comment='评论',
        schema=None
    )
    op.drop_table_comment(
        'commodity',
        existing_comment='商品',
        schema=None
    )
    op.drop_table_comment(
        'order',
        existing_comment='订单',
        schema=None
    )
    op.add_column('user', sa.Column('sex', sa.Integer(), nullable=True))
    op.add_column('user', sa.Column('signature', sa.String(length=100), nullable=True))
    op.drop_table_comment(
        'user',
        existing_comment='用户',
        schema=None
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table_comment(
        'user',
        '用户',
        existing_comment=None,
        schema=None
    )
    op.drop_column('user', 'signature')
    op.drop_column('user', 'sex')
    op.create_table_comment(
        'order',
        '订单',
        existing_comment=None,
        schema=None
    )
    op.create_table_comment(
        'commodity',
        '商品',
        existing_comment=None,
        schema=None
    )
    op.create_table_comment(
        'comment',
        '评论',
        existing_comment=None,
        schema=None
    )
    op.create_table_comment(
        'address',
        '地址',
        existing_comment=None,
        schema=None
    )
    op.drop_column('address', 'tags')
    op.drop_column('address', 'phone')
    op.drop_column('address', 'name')
    op.drop_column('address', 'isdefault')
    # ### end Alembic commands ###