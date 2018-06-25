"""create team table

Revision ID: f2462fa06e38
Revises: ae7b3c550ee9
Create Date: 2018-06-24 14:03:21.536631

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f2462fa06e38'
down_revision = '4576313293b0'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'team',
        sa.Column('id',
            sa.Integer,
            primary_key=True,
            autoincrement=True),

        sa.Column('name',
            sa.String(20),
            nullable=False),

        sa.Column('boundary_id',
            sa.Integer,
            sa.ForeignKey('taskBoundary.id'),
            nullable=False)
    )


def downgrade():
    op.drop_table('team')
