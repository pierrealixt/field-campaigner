"""create featureType table

Revision ID: 8ae064cc9994
Revises: 05ad22ce2161
Create Date: 2018-06-24 11:48:11.862432

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8ae064cc9994'
down_revision = '133d8b6d8f83'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'featureType',
        
        sa.Column('id',
            sa.Integer,
            primary_key=True,
            autoincrement=True),

        sa.Column('feature',
            sa.String(50),
            nullable=False),

        sa.Column('name',
            sa.String(50)),

        sa.Column('is_template',
            sa.BOOLEAN(),
            default=False)
    )


def downgrade():
    op.drop_table('featureType')
