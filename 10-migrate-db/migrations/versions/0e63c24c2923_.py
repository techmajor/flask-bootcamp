"""empty message

Revision ID: 0e63c24c2923
Revises: b199b19872e2
Create Date: 2022-12-07 14:27:29.384591

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '0e63c24c2923'
down_revision = 'b199b19872e2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('dummy', schema=None) as batch_op:
        batch_op.alter_column('description',
               existing_type=mysql.VARCHAR(length=150),
               type_=sa.String(length=200),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('dummy', schema=None) as batch_op:
        batch_op.alter_column('description',
               existing_type=sa.String(length=200),
               type_=mysql.VARCHAR(length=150),
               existing_nullable=True)

    # ### end Alembic commands ###
