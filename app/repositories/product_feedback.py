from __future__ import annotations

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.product import Product
from app.models.product_feedback import ProductComment, ProductRating


class ProductFeedbackRepository:
    def __init__(self, db: Session):
        self.db = db

    # -----------------
    # Ratings
    # -----------------
    def get_user_rating(self, product_id: int, user_id: int) -> ProductRating | None:
        stmt = select(ProductRating).where(
            ProductRating.product_id == product_id,
            ProductRating.user_id == user_id,
        )
        return self.db.scalar(stmt)

    def upsert_rating(self, product: Product, user_id: int, rating: int) -> ProductRating:
        existing = self.get_user_rating(product.id, user_id)
        if existing:
            existing.rating = rating
            self.db.add(existing)
            self.db.commit()
            self.db.refresh(existing)
            self.recalculate_product_rating(product)
            return existing

        obj = ProductRating(product_id=product.id, user_id=user_id, rating=rating)
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        self.recalculate_product_rating(product)
        return obj

    def delete_rating(self, product: Product, user_id: int) -> bool:
        existing = self.get_user_rating(product.id, user_id)
        if not existing:
            return False
        self.db.delete(existing)
        self.db.commit()
        self.recalculate_product_rating(product)
        return True

    def get_rating_stats(self, product_id: int) -> tuple[float, int]:
        stmt = select(
            func.coalesce(func.avg(ProductRating.rating), 0.0),
            func.count(ProductRating.id),
        ).where(ProductRating.product_id == product_id)
        avg_, count_ = self.db.execute(stmt).one()
        return float(avg_ or 0.0), int(count_ or 0)

    def recalculate_product_rating(self, product: Product) -> Product:
        avg_, _count = self.get_rating_stats(product.id)
        # Store average in products.rating so list endpoints are fast.
        product.rating = avg_
        self.db.add(product)
        self.db.commit()
        self.db.refresh(product)
        return product

    # -----------------
    # Comments
    # -----------------
    def create_comment(self, product_id: int, user_id: int, text: str) -> ProductComment:
        obj = ProductComment(product_id=product_id, user_id=user_id, text=text)
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def list_comments(self, product_id: int, skip: int = 0, limit: int = 50) -> list[ProductComment]:
        stmt = (
            select(ProductComment)
            .where(ProductComment.product_id == product_id)
            .order_by(ProductComment.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        return list(self.db.scalars(stmt).all())

    def count_comments(self, product_id: int) -> int:
        stmt = select(func.count()).select_from(ProductComment).where(ProductComment.product_id == product_id)
        return int(self.db.scalar(stmt) or 0)

    def get_comment(self, comment_id: int) -> ProductComment | None:
        return self.db.get(ProductComment, comment_id)

    def delete_comment(self, comment: ProductComment) -> None:
        self.db.delete(comment)
        self.db.commit()
