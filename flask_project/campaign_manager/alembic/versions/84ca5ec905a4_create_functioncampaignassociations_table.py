"""create functionCampaignAssociations table

Revision ID: 84ca5ec905a4
Revises: 860d9a8bb2bf
Create Date: 2018-06-24 14:23:39.447354

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '84ca5ec905a4'
down_revision = '860d9a8bb2bf'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'functionCampaignAssociations',

        sa.Column('campaign_id',
            sa.Integer,
            sa.ForeignKey('campaign.id')),

        sa.Column('function_id',
            sa.Integer,
            sa.ForeignKey('function.id'))
    )


def downgrade():
    op.drop_table('functionCampaignAssociations')
