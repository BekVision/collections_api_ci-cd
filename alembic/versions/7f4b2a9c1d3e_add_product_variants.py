"""add_product_variants

Revision ID: 7f4b2a9c1d3e
Revises: 434f74f0f25d
Create Date: 2026-02-07 12:00:00.000000

"""
from __future__ import annotations

from alembic import op
import sqlalchemy as sa


revision = "7f4b2a9c1d3e"
down_revision = "434f74f0f25d"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "product_variants",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("price", sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column("product_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["product_id"], ["products.id"]),
        sa.PrimaryKeyConstraint("id"),
    )

    op.add_column("order_items", sa.Column("variant_id", sa.Integer(), nullable=True))
    op.create_foreign_key(
        "fk_order_items_variant_id",
        "order_items",
        "product_variants",
        ["variant_id"],
        ["id"],
    )


def downgrade() -> None:
    op.drop_constraint("fk_order_items_variant_id", "order_items", type_="foreignkey")
    op.drop_column("order_items", "variant_id")
    op.drop_table("product_variants")
