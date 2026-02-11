from sqlalchemy.orm import Session

from app.models.order import Order, OrderItem, OrderStatus
from app.repositories.order import OrderRepository
from app.repositories.product import ProductRepository
from app.schemas.order import OrderCreate


class OrderService:
    def __init__(self, db: Session):
        self.db = db
        self.order_repo = OrderRepository(db)
        self.product_repo = ProductRepository(db)

    def create_order(self, user_id: int, payload: OrderCreate):
        items: list[OrderItem] = []
        for item in payload.items:
            if item.quantity <= 0:
                raise ValueError("Quantity must be greater than zero")
            product = self.product_repo.get(item.product_id)
            if not product:
                raise ValueError("Product not found")
            unit_price = product.price
            variant_id = None
            if item.variant_id is not None:
                variant = self.product_repo.get_variant(item.variant_id)
                if not variant or variant.product_id != product.id:
                    raise ValueError("Invalid product variant")
                unit_price = variant.price
                variant_id = variant.id
            items.append(
                OrderItem(
                    product_id=product.id,
                    variant_id=variant_id,
                    quantity=item.quantity,
                    unit_price=unit_price,
                )
            )

        order = Order(user_id=user_id, status=OrderStatus.success, items=items)
        created = self.order_repo.create(order)

        for item in created.items:
            product = self.product_repo.get(item.product_id)
            if product:
                self.product_repo.increment_sold(product, item.quantity)

        return created

    def list_user_orders(self, user_id: int, skip: int, limit: int):
        return self.order_repo.list_by_user(user_id, skip=skip, limit=limit)

    def list_all_orders(self, skip: int, limit: int):
        return self.order_repo.list_all(skip=skip, limit=limit)

    def list_user_orders_paged(self, user_id: int, skip: int, limit: int):
        items = self.order_repo.list_by_user(user_id, skip=skip, limit=limit)
        total = self.order_repo.count_by_user(user_id)
        next_skip = skip + limit if skip + limit < total else None
        return items, total, next_skip

    def list_all_orders_paged(self, skip: int, limit: int):
        items = self.order_repo.list_all(skip=skip, limit=limit)
        total = self.order_repo.count_all()
        next_skip = skip + limit if skip + limit < total else None
        return items, total, next_skip
