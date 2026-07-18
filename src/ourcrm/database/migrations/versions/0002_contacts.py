"""Add contacts table.

Revision ID: 0002_contacts
Revises: 0001_initial
Create Date: 2026-07-18
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0002_contacts"
down_revision: str | None = "0001_initial"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "contacts",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("first_name", sa.String, nullable=False, server_default=""),
        sa.Column("last_name", sa.String, nullable=False, server_default=""),
        sa.Column("email", sa.String, nullable=False, server_default=""),
        sa.Column("phone", sa.String, nullable=False, server_default=""),
        sa.Column("address_street", sa.String, nullable=False, server_default=""),
        sa.Column("address_city", sa.String, nullable=False, server_default=""),
        sa.Column("address_state", sa.String, nullable=False, server_default=""),
        sa.Column("address_zip", sa.String, nullable=False, server_default=""),
        sa.Column("notes", sa.Text, nullable=False, server_default=""),
    )


def downgrade() -> None:
    op.drop_table("contacts")
