"""empty message

Revision ID: 414aa5860481
Revises: 8d4032ef6e06
Create Date: 2024-03-15 14:29:13.102744

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '414aa5860481'
down_revision = '8d4032ef6e06'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('items', schema=None) as batch_op:
        batch_op.add_column(sa.Column('item_description', sa.String(length=512), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('items', schema=None) as batch_op:
        batch_op.drop_column('item_description')

    # ### end Alembic commands ###
