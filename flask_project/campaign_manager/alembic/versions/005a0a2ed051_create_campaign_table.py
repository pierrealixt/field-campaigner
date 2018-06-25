"""create campaign table

Revision ID: 005a0a2ed051
Revises: 
Create Date: 2018-06-23 13:05:46.978621

"""
from alembic import op
import sqlalchemy as sa
from geoalchemy2 import Geometry

# revision identifiers, used by Alembic.
revision = '005a0a2ed051'
down_revision = '2c5801615b10'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'campaign',
        
        sa.Column('id', 
            sa.Integer, 
            primary_key=True, 
            autoincrement=True),
        
        sa.Column('creator_id', 
            sa.Integer, 
            sa.ForeignKey('user.id'), 
            nullable=False),
        
        sa.Column('geometry', 
            Geometry('POLYGON')),
        
        sa.Column('name', 
            sa.String(20), 
            unique=True, 
            nullable=True),
        
        sa.Column('description', 
            sa.String(200)),
        
        sa.Column('start_date', 
            sa.Date(), 
            nullable=False),
        
        sa.Column('end_date', 
            sa.Date(), 
            nullable=False),
        
        sa.Column('create_on', 
            sa.DateTime(), 
            nullable=False),
        
        sa.Column('link_to_OpenMapKit', 
            sa.BOOLEAN(), 
            default=False),
        
        sa.Column('version', 
            sa.Integer),
        
        sa.Column('uuid', 
            sa.String(100)),
        
        sa.Column('remote_projects', 
            sa.String(30)),
        
        sa.Column('map_type', 
            sa.String(20)),
        
        sa.Column('thumbnail', 
            sa.String(100))
    )


def downgrade():
    op.drop_table('campaign')
