from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.deps import get_db, require_admin
from app.schemas.category import CategoryCreate, CategoryListResponse, CategoryRead, CategoryUpdate
from app.services.category import CategoryService

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.get("", response_model=list[CategoryRead])
def list_categories(
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
):
    return CategoryService(db).list_categories(skip, limit)


@router.get("/paged", response_model=CategoryListResponse)
def list_categories_paged(
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
):
    items, total, next_skip = CategoryService(db).list_categories_paged(skip, limit)
    return {
        "items": items,
        "total": total,
        "skip": skip,
        "limit": limit,
        "next_skip": next_skip,
    }


@router.post("", response_model=CategoryRead, status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_admin)])
def create_category(payload: CategoryCreate, db: Session = Depends(get_db)):
    return CategoryService(db).create_category(payload)


@router.put("/{category_id}", response_model=CategoryRead, dependencies=[Depends(require_admin)])
def update_category(category_id: int, payload: CategoryUpdate, db: Session = Depends(get_db)):
    category = CategoryService(db).update_category(category_id, payload)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(require_admin)])
def delete_category(category_id: int, db: Session = Depends(get_db)):
    deleted = CategoryService(db).delete_category(category_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Category not found")
