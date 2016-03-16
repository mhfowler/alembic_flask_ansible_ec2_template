"""create account table

Revision ID: 2c1b8406e85d
Revises: 
Create Date: 2016-03-16 00:44:41.325677

"""

# revision identifiers, used by Alembic.
revision = '2c1b8406e85d'
down_revision = None
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'test',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(50), nullable=False),
        sa.Column('email', sa.String(200), unique=True),
    )
    pass


def downgrade():
    op.drop_table('test')
