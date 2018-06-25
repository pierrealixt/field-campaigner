"""create attribute table

Revision ID: ae7b3c550ee9
Revises: 4576313293b0
Create Date: 2018-06-24 14:00:32.255199

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ae7b3c550ee9'
down_revision = '801e1bf84334'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'attribute',
        sa.Column('id',
            sa.Integer,
            primary_key=True,
            autoincrement=True),

        sa.Column('attribute_name',
            sa.String(50))
    )


def downgrade():
    op.drop_table('attribute')
