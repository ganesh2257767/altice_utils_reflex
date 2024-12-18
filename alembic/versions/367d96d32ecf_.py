"""empty message

Revision ID: 367d96d32ecf
Revises: 
Create Date: 2024-11-03 19:50:18.381143

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
import sqlmodel

# revision identifiers, used by Alembic.
revision: str = '367d96d32ecf'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('messages',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_by', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('message', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('completed', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['created_by'], ['users.email'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('usages',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('used_by', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('service_used', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('used_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['used_by'], ['users.email'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('contact')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('contact',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('created_by', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('message', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    sa.Column('completed', sa.BOOLEAN(), server_default=sa.text('false'), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['created_by'], ['users.email'], name='contact_created_by_fkey'),
    sa.PrimaryKeyConstraint('id', name='contact_pkey')
    )
    op.drop_table('usages')
    op.drop_table('messages')
    # ### end Alembic commands ###
