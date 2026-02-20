from sqlalchemy.orm import Session

from app.models.product import Product
from app.repositories.product import ProductRepository
from app.schemas.product import ProductCreate, ProductUpdate


class ProductService:
    def __init__(self, db: Session):
        self.repo = ProductRepository(db)

    def list_products(
        self,
        query: str | None,
        category_id: int | None,
        price_min: float | None,
        price_max: float | None,
        skip: int,
        limit: int,
    ):
        return self.repo.list(
            query=query,
            category_id=category_id,
            price_min=price_min,
            price_max=price_max,
            skip=skip,
            limit=limit,
        )

    def list_products_paged(
        self,
        query: str | None,
        category_id: int | None,
        price_min: float | None,
        price_max: float | None,
        skip: int,
        limit: int,
    ) -> tuple[list[Product], int, int | None]:
        items = self.repo.list(
            query=query,
            category_id=category_id,
            price_min=price_min,
            price_max=price_max,
            skip=skip,
            limit=limit,
        )
        total = self.repo.count(
            query=query,
            category_id=category_id,
            price_min=price_min,
            price_max=price_max,
        )
        next_skip = skip + limit if skip + limit < total else None
        return items, total, next_skip

    def get_product(self, product_id: int):
        product = self.repo.get(product_id)
        if not product:
            return None
        return self.repo.increment_views(product)

    def create_product(self, payload: ProductCreate):
        product = Product(
            name=payload.name,
            description=payload.description,
            price=payload.price,
            rating=0,
            category_id=payload.category_id,
            stock_count=payload.stock_count,
        )
        created = self.repo.create(product)
        if payload.images:
            self.repo.set_images(created, payload.images)
        if payload.variants:
            self.repo.set_variants(created, [item.model_dump() for item in payload.variants])
        return self.repo.get(created.id)

    def update_product(self, product_id: int, payload: ProductUpdate):
        product = self.repo.get(product_id)
        if not product:
            return None
        if payload.name is not None:
            product.name = payload.name
        if payload.description is not None:
            product.description = payload.description
        if payload.price is not None:
            product.price = payload.price
        if payload.rating is not None:
            product.rating = payload.rating
        if payload.category_id is not None:
            product.category_id = payload.category_id
        if payload.stock_count is not None:
            product.stock_count = payload.stock_count
        updated = self.repo.update(product)
        if payload.images is not None:
            self.repo.set_images(updated, payload.images)
        if payload.variants is not None:
            self.repo.set_variants(updated, [item.model_dump() for item in payload.variants])
        return self.repo.get(updated.id)

    def delete_product(self, product_id: int) -> bool:
        product = self.repo.get(product_id)
        if not product:
            return False
        self.repo.delete(product)
        return True

    def count_products(self) -> int:
        return self.repo.count(
            query=None,
            category_id=None,
            price_min=None,
            price_max=None,
        )