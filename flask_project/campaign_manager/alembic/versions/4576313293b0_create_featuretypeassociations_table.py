"""create featureTypeAssociations table

Revision ID: 4576313293b0
Revises: 801e1bf84334
Create Date: 2018-06-24 13:57:41.123644

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4576313293b0'
down_revision = 'ae7b3c550ee9'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'featureTypeAssociations',

        sa.Column('feature_id',
            sa.Integer,
            sa.ForeignKey('attribute.id')),

        sa.Column('type_id',
            sa.Integer,
            sa.ForeignKey('featureType.id'))
    )


def downgrade():
    op.drop_table('featureTypeAssociations')
