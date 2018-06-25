"""create taskBoundary table

Revision ID: 6c105aef9803
Revises: bab43a338c0a
Create Date: 2018-06-24 13:45:51.250754

"""
from alembic import op
import sqlalchemy as sa
from geoalchemy2 import Geometry

# revision identifiers, used by Alembic.
revision = '6c105aef9803'
down_revision = 'bab43a338c0a'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'taskBoundary',
        sa.Column('id',
            sa.Integer,
            primary_key=True,
            autoincrement=True),

        sa.Column('coordinates',
            Geometry('POLYGON')),

        sa.Column('name',
            sa.String(100)),

        sa.Column('status',
            sa.String(100)),

        sa.Column('type_boundary',
            sa.String(100)),

        sa.Column('campaign_id',
            sa.Integer,
            sa.ForeignKey('campaign.id'),
            nullable=False)
    )


def downgrade():
    op.drop_table('taskBoundary')
