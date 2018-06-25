"""create function table

Revision ID: bab43a338c0a
Revises: 05ad22ce2161
Create Date: 2018-06-24 13:41:07.839553

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bab43a338c0a'
down_revision = '05ad22ce2161'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'function',
        sa.Column('id',
            sa.Integer,
            primary_key=True,
            autoincrement=True),

        sa.Column('name',
            sa.String(100),
            nullable=False),

        sa.Column('feature', 
            sa.String(100)),

        sa.Column('type_id',
            sa.Integer,
            sa.ForeignKey('featureType.id'),
            nullable=False)
    )


def downgrade():
    op.drop_table('function')
