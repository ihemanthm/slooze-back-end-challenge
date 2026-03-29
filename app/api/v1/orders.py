from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.schemas.order import OrderCreate, OrderResponse, OrderCheckout, OrderItemCreate
from app.services.order_service import (
    create_order,
    get_user_orders,
    get_order_by_id,
    checkout_order,
    cancel_order,
    add_items_to_order
)
from app.api.deps import get_current_user, RoleChecker
from app.models.user import User
from app.core.permissions import UserRole

router = APIRouter()


@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_new_order(
    order: OrderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return create_order(db, order, current_user)


@router.get("/", response_model=List[OrderResponse])
def list_orders(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_user_orders(db, current_user)


@router.get("/{order_id}", response_model=OrderResponse)
def get_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    order = get_order_by_id(db, order_id, current_user)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    return order


@router.post("/{order_id}/items", response_model=OrderResponse)
def add_order_items(
    order_id: int,
    items: List[OrderItemCreate],
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return add_items_to_order(db, order_id, items, current_user)


@router.post("/{order_id}/checkout", response_model=OrderResponse)
def checkout(
    order_id: int,
    checkout_data: OrderCheckout,
    db: Session = Depends(get_db),
    current_user: User = Depends(RoleChecker([UserRole.ADMIN, UserRole.MANAGER]))
):
    return checkout_order(db, order_id, checkout_data.payment_method_id, current_user)


@router.delete("/{order_id}", response_model=OrderResponse)
def cancel(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(RoleChecker([UserRole.ADMIN, UserRole.MANAGER]))
):
    return cancel_order(db, order_id, current_user)
