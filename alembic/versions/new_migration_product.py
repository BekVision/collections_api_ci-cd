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