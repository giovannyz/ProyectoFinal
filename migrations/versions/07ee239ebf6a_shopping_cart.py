"""shopping cart

Revision ID: 07ee239ebf6a
Revises: 25b2cd870b1d
Create Date: 2023-03-07 16:29:55.680733

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '07ee239ebf6a'
down_revision = '25b2cd870b1d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('shopping_cart',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('product_id', sa.Integer(), nullable=True),
    sa.Column('quantity', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('pedido', schema=None) as batch_op:
        batch_op.alter_column('total_price',
               existing_type=sa.REAL(),
               type_=sa.Float(precision=2),
               existing_nullable=True)

    with op.batch_alter_table('pedido_items', schema=None) as batch_op:
        batch_op.alter_column('price',
               existing_type=sa.REAL(),
               type_=sa.Float(precision=2),
               existing_nullable=True)

    with op.batch_alter_table('products', schema=None) as batch_op:
        batch_op.alter_column('precio',
               existing_type=sa.REAL(),
               type_=sa.Float(precision=2),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('products', schema=None) as batch_op:
        batch_op.alter_column('precio',
               existing_type=sa.Float(precision=2),
               type_=sa.REAL(),
               existing_nullable=True)

    with op.batch_alter_table('pedido_items', schema=None) as batch_op:
        batch_op.alter_column('price',
               existing_type=sa.Float(precision=2),
               type_=sa.REAL(),
               existing_nullable=True)

    with op.batch_alter_table('pedido', schema=None) as batch_op:
        batch_op.alter_column('total_price',
               existing_type=sa.Float(precision=2),
               type_=sa.REAL(),
               existing_nullable=True)

    op.drop_table('shopping_cart')
    # ### end Alembic commands ###
