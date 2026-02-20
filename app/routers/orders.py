from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.deps import get_current_user, get_db, require_admin
from app.schemas.order import OrderCreate, OrderListResponse, OrderRead
from app.services.order import OrderService
from app.schemas.order import OrderStatusUpdate
from app.models.order import OrderStatus

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.post("", response_model=OrderRead, status_code=status.HTTP_201_CREATED)
def create_order(payload: OrderCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    try:
        return OrderService(db).create_order(current_user.id, payload)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.get("/me", response_model=list[OrderRead])
def list_my_orders(
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return OrderService(db).list_user_orders(current_user.id, skip, limit)


@router.get("/me/paged", response_model=OrderListResponse)
def list_my_orders_paged(
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    items, total, next_skip = OrderService(db).list_user_orders_paged(
        current_user.id,
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


@router.get("", response_model=list[OrderRead], dependencies=[Depends(require_admin)])
def list_all_orders(
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
):
    return OrderService(db).list_all_orders(skip, limit)


@router.get("/paged", response_model=OrderListResponse, dependencies=[Depends(require_admin)])
def list_all_orders_paged(
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
):
    items, total, next_skip = OrderService(db).list_all_orders_paged(skip, limit)
    return {
        "items": items,
        "total": total,
        "skip": skip,
        "limit": limit,
        "next_skip": next_skip,
    }


@router.put("/{order_id}/status", response_model=OrderRead, dependencies=[Depends(require_admin)])
def update_order_status(order_id: int, payload: OrderStatusUpdate, db: Session = Depends(get_db)):
    try:
        # payload.status string -> enum
        new_status = OrderStatus(payload.status)
        return OrderService(db).update_status(order_id, new_status)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))