from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query, status, UploadFile, File, Form
from sqlalchemy.orm import Session

from app.core.deps import get_db, require_admin
from app.schemas.product import ProductCreate, ProductListResponse, ProductRead, ProductUpdate
from app.services.product import ProductService
from app.utils.file_upload import save_file

router = APIRouter(prefix="/products", tags=["Products"])


@router.get("", response_model=list[ProductRead])
def list_products(
    q: str | None = None,
    category_id: int | None = None,
    price_min: float | None = Query(default=None, ge=0),
    price_max: float | None = Query(default=None, ge=0),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=50, ge=1, le=200),
    db: Session = Depends(get_db),
):
    return ProductService(db).list_products(q, category_id, price_min, price_max, skip, limit)


@router.get("/paged", response_model=ProductListResponse)
def list_products_paged(
    q: str | None = None,
    category_id: int | None = None,
    price_min: float | None = Query(default=None, ge=0),
    price_max: float | None = Query(default=None, ge=0),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=50, ge=1, le=200),
    db: Session = Depends(get_db),
):
    items, total, next_skip = ProductService(db).list_products_paged(
        q,
        category_id,
        price_min,
        price_max,
        skip,
        limit,
    )
    return {
        "items": items,
        "total": total,
        "skip": skip,
        "limit": limit,
        "next_skip": next_skip,
    }


@router.get("/{product_id}", response_model=ProductRead)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = ProductService(db).get_product(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.get("/count")
def products_count(db: Session = Depends(get_db)):
    total = ProductService(db).count_products()
    return {"total": total}

@router.post("", response_model=ProductRead, status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_admin)])
def create_product(payload: ProductCreate, db: Session = Depends(get_db)):
    return ProductService(db).create_product(payload)


@router.post(
    "/with-image",
    response_model=ProductRead,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_admin)],
)
async def create_product_with_images(
    name: str = Form(...),
    description: str = Form(...),
    price: float = Form(...),
    rating: float = Form(0),
    category_id: int = Form(...),
    stock_count: int = Form(0),

    # old: image: UploadFile = File(...)
    images: List[UploadFile] = File(...),

    db: Session = Depends(get_db),
):
    # ✅ max 4 ta
    if len(images) > 4:
        raise HTTPException(status_code=400, detail="Maximum 4 images allowed")

    allowed = {"image/jpeg", "image/png", "image/webp"}
    for img in images:
        if img.content_type not in allowed:
            raise HTTPException(status_code=400, detail=f"Invalid file type: {img.content_type}")

    image_urls = []
    for img in images:
        url = await save_file(img)
        image_urls.append(url)

    payload = ProductCreate(
        name=name,
        description=description,
        price=price,
        rating=rating,
        category_id=category_id,
        stock_count=stock_count,
        images=image_urls,
        variants=[],
    )
    return ProductService(db).create_product(payload)


@router.put("/{product_id}", response_model=ProductRead, dependencies=[Depends(require_admin)])
def update_product(product_id: int, payload: ProductUpdate, db: Session = Depends(get_db)):
    product = ProductService(db).update_product(product_id, payload)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(require_admin)])
def delete_product(product_id: int, db: Session = Depends(get_db)):
    deleted = ProductService(db).delete_product(product_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Product not found")
    return
