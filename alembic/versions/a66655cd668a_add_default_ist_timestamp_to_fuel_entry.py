"""Add default IST timestamp to fuel_entry

Revision ID: a66655cd668a
Revises: a52a66c46698
Create Date: 2025-12-12 15:15:58.437299

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a66655cd668a'
down_revision: Union[str, Sequence[str], None] = 'a52a66c46698'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add server default for IST timestamp
    op.alter_column(
        'fuel_entry',
        'date_of_fuel_entry',
        server_default=sa.text("timezone('Asia/Kolkata', now())"),
        existing_type=sa.DateTime(timezone=True),
        existing_nullable=False,
    )



def downgrade() -> None:
    op.alter_column(
        'fuel_entry',
        'date_of_fuel_entry',
        server_default=None,
        existing_type=sa.DateTime(timezone=True),
        existing_nullable=False,
    )

