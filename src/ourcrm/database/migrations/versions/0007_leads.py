"""Add leads table.

Revision ID: 0007_leads
Revises: 0006_call_outcomes_callback_range
Create Date: 2026-08-30
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0007_leads"
down_revision: str | None = "0006_call_outcomes_callback_range"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "leads",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("name", sa.String, nullable=False, server_default=""),
        sa.Column("email", sa.String, nullable=False, server_default=""),
        sa.Column("phone", sa.String, nullable=False, server_default=""),
        sa.Column("status", sa.String, nullable=False, server_default=""),
        sa.Column("source", sa.String, nullable=False, server_default=""),
        sa.Column("budget_min", sa.Integer, nullable=True),
        sa.Column("budget_max", sa.Integer, nullable=True),
        sa.Column("desired_location", sa.String, nullable=False, server_default=""),
        sa.Column("property_type", sa.String, nullable=False, server_default=""),
        sa.Column("timeline", sa.String, nullable=False, server_default=""),
        sa.Column("notes", sa.Text, nullable=False, server_default=""),
    )


def downgrade() -> None:
    op.drop_table("leads")
