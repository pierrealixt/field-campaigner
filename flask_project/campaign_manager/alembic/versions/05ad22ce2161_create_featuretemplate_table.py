"""create featureTemplate table

Revision ID: 05ad22ce2161
Revises: 133d8b6d8f83
Create Date: 2018-06-24 11:44:27.175172

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '05ad22ce2161'
down_revision = '8ae064cc9994'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'featureTemplate',
      
        sa.Column('id', 
            sa.Integer, 
            primary_key=True, 
            autoincrement=True),

        sa.Column('name',
            sa.String(50),
            nullable=False),

        sa.Column('description',
            sa.String(200)),

        sa.Column('featureType_id',
            sa.Integer,
            sa.ForeignKey('featureType.id'))
    )


def downgrade():
    op.drop_table('featureTemplate')
