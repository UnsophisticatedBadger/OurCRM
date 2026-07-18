"""Add tags column to contacts.

Revision ID: 0003_contact_tags
Revises: 0002_contacts
Create Date: 2026-07-18
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0003_contact_tags"
down_revision: str | None = "0002_contacts"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column("contacts", sa.Column("tags", sa.Text, nullable=False, server_default=""))


def downgrade() -> None:
    op.drop_column("contacts", "tags")
