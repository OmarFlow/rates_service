"""init

Revision ID: d784882b80e9
Revises: 
Create Date: 2023-11-05 12:27:15.630282

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd784882b80e9'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('symbol',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('symbol_history',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('symbol_id', sa.Integer(), nullable=True),
    sa.Column('exchanger', sa.String(), server_default='binance', nullable=False),
    sa.Column('value', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['symbol_id'], ['symbol.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('symbol_history')
    op.drop_table('symbol')
    # ### end Alembic commands ###
