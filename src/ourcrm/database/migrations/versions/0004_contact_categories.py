"""Add categories table and category_id column on contacts.

Revision ID: 0004_contact_categories
Revises: 0003_contact_tags
Create Date: 2026-07-24
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0004_contact_categories"
down_revision: str | None = "0003_contact_tags"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_DEFAULT_CATEGORIES = [
    "Past Client",
    "Current Client",
    "Prospect",
    "Vendor",
    "Referral Partner",
    "Other",
]


def upgrade() -> None:
    categories_table = op.create_table(
        "categories",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("name", sa.String, nullable=False, unique=True),
    )
    op.bulk_insert(categories_table, [{"name": name} for name in _DEFAULT_CATEGORIES])
    with op.batch_alter_table("contacts") as batch_op:
        batch_op.add_column(sa.Column("category_id", sa.Integer, nullable=True))
        batch_op.create_foreign_key(
            "fk_contacts_category_id_categories", "categories", ["category_id"], ["id"]
        )


def downgrade() -> None:
    with op.batch_alter_table("contacts") as batch_op:
        batch_op.drop_constraint("fk_contacts_category_id_categories", type_="foreignkey")
        batch_op.drop_column("category_id")
    op.drop_table("categories")
