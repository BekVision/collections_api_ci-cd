from typing import Sequence

from sqlalchemy import func, select
from sqlalchemy.orm import Session, selectinload

from app.models.product import Product, ProductImage, ProductVariant


class ProductRepository:
    def __init__(self, db: Session):
        self.db = db

    def _apply_filters(
        self,
        stmt,
        query: str | None = None,
        category_id: int | None = None,
        price_min: float | None = None,
        price_max: float | None = None,
    ):
        if query:
            stmt = stmt.where(Product.name.ilike(f"%{query}%"))
        if category_id:
            stmt = stmt.where(Product.category_id == category_id)
        if price_min is not None:
            stmt = stmt.where(Product.price >= price_min)
        if price_max is not None:
            stmt = stmt.where(Product.price <= price_max)
        return stmt

    def list(
        self,
        query: str | None = None,
        category_id: int | None = None,
        price_min: float | None = None,
        price_max: float | None = None,
        skip: int = 0,
        limit: int = 50,
    ) -> list[Product]:
        stmt = select(Product).options(
            selectinload(Product.images),
            selectinload(Product.category),
            selectinload(Product.variants),
        )
        stmt = self._apply_filters(
            stmt,
            query=query,
            category_id=category_id,
            price_min=price_min,
            price_max=price_max,
        )
        stmt = stmt.offset(skip).limit(limit)
        return list(self.db.scalars(stmt).all())

    def count(
        self,
        query: str | None = None,
        category_id: int | None = None,
        price_min: float | None = None,
        price_max: float | None = None,
    ) -> int:
        stmt = select(func.count()).select_from(Product)
        stmt = self._apply_filters(
            stmt,
            query=query,
            category_id=category_id,
            price_min=price_min,
            price_max=price_max,
        )
        return int(self.db.scalar(stmt) or 0)

    def get(self, product_id: int) -> Product | None:
        stmt = (
            select(Product)
            .where(Product.id == product_id)
            .options(
                selectinload(Product.images),
                selectinload(Product.category),
                selectinload(Product.variants),
            )
        )
        return self.db.scalar(stmt)

    def create(self, product: Product) -> Product:
        self.db.add(product)
        self.db.commit()
        self.db.refresh(product)
        return product

    def update(self, product: Product) -> Product:
        self.db.add(product)
        self.db.commit()
        self.db.refresh(product)
        return product

    def delete(self, product: Product) -> None:
        self.db.delete(product)
        self.db.commit()

    def set_images(self, product: Product, images: Sequence[str]) -> Product:
        product.images = [ProductImage(url=url) for url in images]
        self.db.add(product)
        self.db.commit()
        self.db.refresh(product)
        return product

    def set_variants(self, product: Product, variants: Sequence[dict]) -> Product:
        product.variants = [
            ProductVariant(name=item["name"], price=item["price"]) for item in variants
        ]
        self.db.add(product)
        self.db.commit()
        self.db.refresh(product)
        return product

    def get_variant(self, variant_id: int) -> ProductVariant | None:
        return self.db.get(ProductVariant, variant_id)

    def increment_views(self, product: Product) -> Product:
        product.views_count += 1
        self.db.add(product)
        self.db.commit()
        self.db.refresh(product)
        return product

    def increment_sold(self, product: Product, quantity: int) -> Product:
        product.sold_count += quantity
        self.db.add(product)
        self.db.commit()
        self.db.refresh(product)
        return product
