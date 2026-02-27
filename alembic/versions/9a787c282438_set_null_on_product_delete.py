"""set null on product delete

Revision ID: 9a787c282438
Revises: 7f4b2a9c1d3e
Create Date: 2026-02-27 10:55:07.836101

"""
from __future__ import annotations

from alembic import op
import sqlalchemy as sa



revision = '9a787c282438'
down_revision = '7f4b2a9c1d3e'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa

def upgrade():
    # product_id nullable
    op.alter_column(
        "order_items",
        "product_id",
        existing_type=sa.Integer(),
        nullable=True
    )

    # FK drop
    op.drop_constraint(
        "order_items_product_id_fkey",
        "order_items",
        type_="foreignkey"
    )

    # FK recreate with SET NULL
    op.create_foreign_key(
        "order_items_product_id_fkey",
        "order_items",
        "products",
        ["product_id"],
        ["id"],
        ondelete="SET NULL"
    )

def downgrade():
    op.drop_constraint(
        "order_items_product_id_fkey",
        "order_items",
        type_="foreignkey"
    )

    op.create_foreign_key(
        "order_items_product_id_fkey",
        "order_items",
        "products",
        ["product_id"],
        ["id"]
    )

    op.alter_column(
        "order_items",
        "product_id",
        existing_type=sa.Integer(),
        nullable=False
    )