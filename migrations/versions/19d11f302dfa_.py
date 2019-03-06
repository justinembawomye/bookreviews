"""empty message

Revision ID: 19d11f302dfa
Revises: 6faa9591e121
Create Date: 2019-03-06 10:02:00.674797

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '19d11f302dfa'
down_revision = '6faa9591e121'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('reviews', sa.Column('book_id', sa.Integer(), nullable=False))
    op.alter_column('reviews', 'user_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.create_foreign_key(None, 'reviews', 'users', ['user_id'], ['id'])
    op.create_foreign_key(None, 'reviews', 'books', ['book_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'reviews', type_='foreignkey')
    op.drop_constraint(None, 'reviews', type_='foreignkey')
    op.alter_column('reviews', 'user_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.drop_column('reviews', 'book_id')
    # ### end Alembic commands ###
