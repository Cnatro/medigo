"""refactor db"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = '0f909c6cbd47'
down_revision = 'fa1d319e8809'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("""
        ALTER TABLE chat_messages
        ALTER COLUMN message
        TYPE JSONB
        USING message::jsonb
    """)


def downgrade():
    op.execute("""
        ALTER TABLE chat_messages
        ALTER COLUMN message
        TYPE TEXT
        USING message::text
    """)