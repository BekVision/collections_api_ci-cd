from __future__ import annotations

from sqlalchemy.orm import Session

from app.repositories.product import ProductRepository
from app.repositories.product_feedback import ProductFeedbackRepository


class ProductFeedbackService:
    def __init__(self, db: Session):
        self.db = db
        self.products = ProductRepository(db)
        self.feedback = ProductFeedbackRepository(db)

    # Ratings
    def upsert_rating(self, product_id: int, user_id: int, rating: int):
        product = self.products.get(product_id)
        if not product:
            return None
        return self.feedback.upsert_rating(product, user_id, rating)

    def delete_my_rating(self, product_id: int, user_id: int) -> bool | None:
        product = self.products.get(product_id)
        if not product:
            return None
        return self.feedback.delete_rating(product, user_id)

    def get_rating_stats(self, product_id: int) -> tuple[float, int] | None:
        product = self.products.get(product_id)
        if not product:
            return None
        return self.feedback.get_rating_stats(product_id)

    def get_my_rating(self, product_id: int, user_id: int) -> int | None:
        product = self.products.get(product_id)
        if not product:
            return None
        existing = self.feedback.get_user_rating(product_id, user_id)
        return existing.rating if existing else None

    # Comments
    def add_comment(self, product_id: int, user_id: int, text: str):
        product = self.products.get(product_id)
        if not product:
            return None
        return self.feedback.create_comment(product_id, user_id, text)

    def list_comments_paged(self, product_id: int, skip: int, limit: int):
        product = self.products.get(product_id)
        if not product:
            return None
        items = self.feedback.list_comments(product_id, skip=skip, limit=limit)
        total = self.feedback.count_comments(product_id)
        next_skip = skip + limit if skip + limit < total else None
        return items, total, next_skip

    def delete_comment(self, product_id: int, comment_id: int, current_user) -> bool | None:
        product = self.products.get(product_id)
        if not product:
            return None

        comment = self.feedback.get_comment(comment_id)
        if not comment or comment.product_id != product_id:
            return False

        if (comment.user_id != current_user.id) and (not current_user.is_admin):
            return False

        self.feedback.delete_comment(comment)
        return True
