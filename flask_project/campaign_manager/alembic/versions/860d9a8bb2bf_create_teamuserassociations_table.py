"""create teamUserAssociations table

Revision ID: 860d9a8bb2bf
Revises: f2462fa06e38
Create Date: 2018-06-24 14:16:08.844644

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '860d9a8bb2bf'
down_revision = 'f2462fa06e38'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'teamUserAssociations',
        sa.Column('user_id',
            sa.Integer,
            sa.ForeignKey('user.id')),
        sa.Column('team_id',
            sa.Integer,
            sa.ForeignKey('team.id'))
    )


def downgrade():
    op.drop_table('teamUserAssociations')
