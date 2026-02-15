from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.deps import get_current_user, get_db
from app.schemas.product_feedback import (
    ProductCommentCreate,
    ProductCommentListResponse,
    ProductCommentRead,
    ProductRatingMy,
    ProductRatingStats,
    ProductRatingUpsert,
)
from app.services.product_feedback import ProductFeedbackService


router = APIRouter(prefix="/products", tags=["Product Feedback"])


# -----------------
# Ratings
# -----------------
@router.get("/{product_id}/rating", response_model=ProductRatingStats)
def get_rating_stats(product_id: int, db: Session = Depends(get_db)):
    stats = ProductFeedbackService(db).get_rating_stats(product_id)
    if stats is None:
        raise HTTPException(status_code=404, detail="Product not found")
    avg_, count_ = stats
    return {"product_id": product_id, "average": avg_, "count": count_}


@router.get("/{product_id}/my-rating", response_model=ProductRatingMy)
def get_my_rating(
    product_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    svc = ProductFeedbackService(db)
    rating = svc.get_my_rating(product_id, current_user.id)
    if rating is None and svc.get_rating_stats(product_id) is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"product_id": product_id, "rating": rating}


@router.post("/{product_id}/rating", status_code=status.HTTP_201_CREATED)
def upsert_rating(
    product_id: int,
    payload: ProductRatingUpsert,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    if payload.rating < 1 or payload.rating > 5:
        raise HTTPException(status_code=422, detail="rating must be between 1 and 5")
    obj = ProductFeedbackService(db).upsert_rating(product_id, current_user.id, payload.rating)
    if obj is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "ok"}


@router.delete("/{product_id}/rating", status_code=status.HTTP_204_NO_CONTENT)
def delete_my_rating(
    product_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    result = ProductFeedbackService(db).delete_my_rating(product_id, current_user.id)
    if result is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return


# -----------------
# Comments
# -----------------
@router.get("/{product_id}/comments", response_model=ProductCommentListResponse)
def list_comments(
    product_id: int,
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=50, ge=1, le=200),
    db: Session = Depends(get_db),
):
    res = ProductFeedbackService(db).list_comments_paged(product_id, skip, limit)
    if res is None:
        raise HTTPException(status_code=404, detail="Product not found")
    items, total, next_skip = res
    return {"items": items, "total": total, "skip": skip, "limit": limit, "next_skip": next_skip}


@router.post(
    "/{product_id}/comments",
    response_model=ProductCommentRead,
    status_code=status.HTTP_201_CREATED,
)
def add_comment(
    product_id: int,
    payload: ProductCommentCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    text = (payload.text or "").strip()
    if len(text) < 1:
        raise HTTPException(status_code=422, detail="text is required")
    if len(text) > 2000:
        raise HTTPException(status_code=422, detail="text is too long (max 2000)")
    comment = ProductFeedbackService(db).add_comment(product_id, current_user.id, text)
    if comment is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return comment


@router.delete("/{product_id}/comments/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_comment(
    product_id: int,
    comment_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    result = ProductFeedbackService(db).delete_comment(product_id, comment_id, current_user)
    if result is None:
        raise HTTPException(status_code=404, detail="Product not found")
    if result is False:
        raise HTTPException(status_code=403, detail="You cannot delete this comment")
    return
