"""create typeCampaignAssociations table

Revision ID: 801e1bf84334
Revises: 6c105aef9803
Create Date: 2018-06-24 13:55:18.565332

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '801e1bf84334'
down_revision = '6c105aef9803'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'typeCampaignAssociations',

        sa.Column('campaign_id',
            sa.Integer,
            sa.ForeignKey('campaign.id'),
            primary_key=True),

        sa.Column('type_id',
            sa.Integer,
            sa.ForeignKey('featureType.id'),
            primary_key=True)
    )


def downgrade():
    op.drop_table('typeCampaignAssociations')
