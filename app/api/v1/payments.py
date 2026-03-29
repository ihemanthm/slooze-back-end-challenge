from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.schemas.payment import PaymentMethodCreate, PaymentMethodUpdate, PaymentMethodResponse
from app.services.payment_service import (
    create_payment_method,
    get_payment_methods,
    update_payment_method,
    delete_payment_method
)
from app.api.deps import get_current_user, RoleChecker
from app.models.user import User
from app.core.permissions import UserRole

router = APIRouter()


@router.post("/", response_model=PaymentMethodResponse, status_code=status.HTTP_201_CREATED)
def create_payment(
    payment: PaymentMethodCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(RoleChecker([UserRole.ADMIN]))
):
    return create_payment_method(db, payment, current_user)


@router.get("/", response_model=List[PaymentMethodResponse])
def list_payment_methods(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_payment_methods(db, current_user)


@router.put("/{payment_id}", response_model=PaymentMethodResponse)
def update_payment(
    payment_id: int,
    payment: PaymentMethodUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(RoleChecker([UserRole.ADMIN]))
):
    return update_payment_method(db, payment_id, payment, current_user)


@router.delete("/{payment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_payment(
    payment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(RoleChecker([UserRole.ADMIN]))
):
    delete_payment_method(db, payment_id, current_user)
    return None
