"""Add pipeline stage columns to leads.

Revision ID: 0008_leads_pipeline_stage
Revises: 0007_leads
Create Date: 2026-09-05
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0008_leads_pipeline_stage"
down_revision: str | None = "0007_leads"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "leads",
        sa.Column("stage", sa.String, nullable=False, server_default="New Lead"),
    )
    op.add_column(
        "leads",
        sa.Column("stage_reason", sa.String, nullable=False, server_default=""),
    )


def downgrade() -> None:
    op.drop_column("leads", "stage_reason")
    op.drop_column("leads", "stage")
