"""add stock_count to products

Revision ID: 05a9efcb7e24
Revises: 9cb042d33022
Create Date: 2026-02-23 17:21:12.353058

"""
from __future__ import annotations

from alembic import op
import sqlalchemy as sa
from alembic import op
import sqlalchemy as sa


revision = '05a9efcb7e24'
down_revision = '9cb042d33022'
branch_labels = None
depends_on = None


from alembic import op
import sqlalchemy as sa
from sqlalchemy import text

def upgrade():
    bind = op.get_bind()
    exists = bind.execute(text("""
        SELECT 1
        FROM information_schema.columns
        WHERE table_name='products' AND column_name='stock_count'
    """)).first()

    if not exists:
        op.add_column(
            "products",
            sa.Column("stock_count", sa.Integer(), nullable=False, server_default="0")
        )

def downgrade():
    bind = op.get_bind()
    exists = bind.execute(text("""
        SELECT 1
        FROM information_schema.columns
        WHERE table_name='products' AND column_name='stock_count'
    """)).first()

    if exists:
        op.drop_column("products", "stock_count")