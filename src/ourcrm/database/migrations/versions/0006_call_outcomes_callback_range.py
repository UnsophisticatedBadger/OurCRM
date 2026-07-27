"""Add callback date range columns to call_outcomes.

Revision ID: 0006_call_outcomes_callback_range
Revises: 0005_call_outcomes
Create Date: 2026-07-27
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0006_call_outcomes_callback_range"
down_revision: str | None = "0005_call_outcomes"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column("call_outcomes", sa.Column("callback_start_date", sa.Date, nullable=True))
    op.add_column("call_outcomes", sa.Column("callback_end_date", sa.Date, nullable=True))


def downgrade() -> None:
    op.drop_column("call_outcomes", "callback_end_date")
    op.drop_column("call_outcomes", "callback_start_date")
