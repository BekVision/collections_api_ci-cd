from sqlalchemy.orm import Session

from app.models.category import Category
from app.repositories.category import CategoryRepository
from app.schemas.category import CategoryCreate, CategoryUpdate


class CategoryService:
    def __init__(self, db: Session):
        self.repo = CategoryRepository(db)

    def list_categories(self, skip: int, limit: int):
        return self.repo.list(skip=skip, limit=limit)

    def list_categories_paged(self, skip: int, limit: int) -> tuple[list[Category], int, int | None]:
        items = self.repo.list(skip=skip, limit=limit)
        total = self.repo.count()
        next_skip = skip + limit if skip + limit < total else None
        return items, total, next_skip

    def create_category(self, payload: CategoryCreate):
        category = Category(name=payload.name)
        return self.repo.create(category)

    def update_category(self, category_id: int, payload: CategoryUpdate):
        category = self.repo.get(category_id)
        if not category:
            return None
        category.name = payload.name
        return self.repo.update(category)

    def delete_category(self, category_id: int) -> bool:
        category = self.repo.get(category_id)
        if not category:
            return False
        self.repo.delete(category)
        return True
