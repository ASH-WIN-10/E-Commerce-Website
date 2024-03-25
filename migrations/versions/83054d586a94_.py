"""empty message

Revision ID: 83054d586a94
Revises: 
Create Date: 2024-03-25 16:57:42.026227

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '83054d586a94'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=False),
    sa.Column('email', sa.String(length=128), nullable=False),
    sa.Column('password_hash', sa.String(length=256), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_user_email'), ['email'], unique=True)

    op.create_table('item',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('item_name', sa.String(length=64), nullable=False),
    sa.Column('item_description', sa.String(length=512), nullable=True),
    sa.Column('price', sa.Integer(), nullable=False),
    sa.Column('img_url', sa.String(), nullable=True),
    sa.Column('quantity', sa.Integer(), nullable=False),
    sa.Column('owner_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['owner_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('item', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_item_owner_id'), ['owner_id'], unique=False)

    op.create_table('cart',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('quantity', sa.Integer(), nullable=False),
    sa.Column('item_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['item_id'], ['item.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('cart', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_cart_item_id'), ['item_id'], unique=True)
        batch_op.create_index(batch_op.f('ix_cart_user_id'), ['user_id'], unique=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('cart', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_cart_user_id'))
        batch_op.drop_index(batch_op.f('ix_cart_item_id'))

    op.drop_table('cart')
    with op.batch_alter_table('item', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_item_owner_id'))

    op.drop_table('item')
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_user_email'))

    op.drop_table('user')
    # ### end Alembic commands ###
