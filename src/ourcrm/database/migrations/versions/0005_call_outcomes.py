"""Add call_outcomes table.

Revision ID: 0005_call_outcomes
Revises: 0004_contact_categories
Create Date: 2026-07-25
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0005_call_outcomes"
down_revision: str | None = "0004_contact_categories"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "call_outcomes",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("contact_id", sa.Integer, sa.ForeignKey("contacts.id"), nullable=False),
        sa.Column("outcome", sa.String, nullable=False),
        sa.Column("logged_at", sa.DateTime, nullable=False),
    )


def downgrade() -> None:
    op.drop_table("call_outcomes")
