from sqlalchemy import desc, select
from sqlalchemy.orm import Session, selectinload

from app.models.product import Product


class RecommendationService:
    def __init__(self, db: Session):
        self.db = db

    def most_viewed(self, limit: int = 10):
        stmt = (
            select(Product)
            .order_by(desc(Product.views_count))
            .limit(limit)
            .options(selectinload(Product.images), selectinload(Product.category))
        )
        return list(self.db.scalars(stmt).all())

    def most_sold(self, limit: int = 10):
        stmt = (
            select(Product)
            .order_by(desc(Product.sold_count))
            .limit(limit)
            .options(selectinload(Product.images), selectinload(Product.category))
        )
        return list(self.db.scalars(stmt).all())
