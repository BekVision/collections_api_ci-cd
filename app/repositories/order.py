from sqlalchemy import func, select
from sqlalchemy.orm import Session, selectinload

from app.models.order import Order, OrderItem
from app.models.product import Product


class OrderRepository:
    def __init__(self, db: Session):
        self.db = db

    def list_all(self, skip: int = 0, limit: int = 50) -> list[Order]:
        stmt = select(Order).options(
            selectinload(Order.items)
            .selectinload(OrderItem.product)
            .selectinload(Product.images),
            selectinload(Order.items)
            .selectinload(OrderItem.product)
            .selectinload(Product.category),
            selectinload(Order.items).selectinload(OrderItem.variant),
        ).offset(skip).limit(limit)
        return list(self.db.scalars(stmt).all())

    def count_all(self) -> int:
        stmt = select(func.count()).select_from(Order)
        return int(self.db.scalar(stmt) or 0)

    def list_by_user(self, user_id: int, skip: int = 0, limit: int = 50) -> list[Order]:
        stmt = (
            select(Order)
            .where(Order.user_id == user_id)
            .options(
                selectinload(Order.items)
                .selectinload(OrderItem.product)
                .selectinload(Product.images),
                selectinload(Order.items)
                .selectinload(OrderItem.product)
                .selectinload(Product.category),
                selectinload(Order.items).selectinload(OrderItem.variant),
            )
            .offset(skip)
            .limit(limit)
        )
        return list(self.db.scalars(stmt).all())

    def count_by_user(self, user_id: int) -> int:
        stmt = select(func.count()).select_from(Order).where(Order.user_id == user_id)
        return int(self.db.scalar(stmt) or 0)

    def create(self, order: Order) -> Order:
        self.db.add(order)
        self.db.commit()
        self.db.refresh(order)
        return order
