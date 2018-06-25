"""create user table

Revision ID: 2c5801615b10
Revises: 005a0a2ed051
Create Date: 2018-06-23 13:36:25.959872

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2c5801615b10'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'user',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('osm_user_id', sa.String(20), unique=True, nullable=True),
        sa.Column('email', sa.String(40))
    )


def downgrade():
    op.drop_table('user')
