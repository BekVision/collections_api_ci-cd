from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session

from app.core.deps import get_db, require_admin
from app.schemas.category import CategoryCreate, CategoryListResponse, CategoryRead, CategoryUpdate
from app.services.category import CategoryService
from app.utils.file_upload import save_file

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


@router.post(
    "/with-icon",
    response_model=CategoryRead,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_admin)],
)
async def create_category_with_icon(
    name: str = Form(...),
    icon: UploadFile | None = File(None),
    db: Session = Depends(get_db),
):
    icon_url = await save_file(icon) if icon else None
    return CategoryService(db).create_category(CategoryCreate(name=name, icon_url=icon_url))


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
    return
