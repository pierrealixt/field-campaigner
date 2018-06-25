"""create adminAssociations table

Revision ID: 133d8b6d8f83
Revises: 005a0a2ed051
Create Date: 2018-06-24 11:41:06.600789

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '133d8b6d8f83'
down_revision = '005a0a2ed051'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
      'adminAssociations',
      sa.Column('user_id', sa.Integer, sa.ForeignKey('user.id')),
      sa.Column('campaign_id', sa.Integer, sa.ForeignKey('campaign.id'))
    )


def downgrade():
    op.drop_table('adminAssociations')
