from sqlalchemy.orm import Session
from app.models.payment import PaymentMethod
from app.models.user import User
from app.schemas.payment import PaymentMethodCreate, PaymentMethodUpdate
from fastapi import HTTPException, status
from typing import List


def create_payment_method(db: Session, payment_data: PaymentMethodCreate, current_user: User) -> PaymentMethod:
    if payment_data.is_default:
        db.query(PaymentMethod).filter(
            PaymentMethod.user_id == current_user.id,
            PaymentMethod.is_default == True
        ).update({"is_default": False})
    
    payment_method = PaymentMethod(
        user_id=current_user.id,
        method_type=payment_data.method_type,
        details=payment_data.details,
        is_default=payment_data.is_default
    )
    db.add(payment_method)
    db.commit()
    db.refresh(payment_method)
    return payment_method


def get_payment_methods(db: Session, current_user: User) -> List[PaymentMethod]:
    return db.query(PaymentMethod).filter(PaymentMethod.user_id == current_user.id).all()


def get_payment_method_by_id(db: Session, payment_id: int, current_user: User) -> PaymentMethod | None:
    return db.query(PaymentMethod).filter(
        PaymentMethod.id == payment_id,
        PaymentMethod.user_id == current_user.id
    ).first()


def update_payment_method(
    db: Session,
    payment_id: int,
    payment_data: PaymentMethodUpdate,
    current_user: User
) -> PaymentMethod:
    payment_method = get_payment_method_by_id(db, payment_id, current_user)
    if not payment_method:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payment method not found"
        )
    
    if payment_data.is_default:
        db.query(PaymentMethod).filter(
            PaymentMethod.user_id == current_user.id,
            PaymentMethod.is_default == True,
            PaymentMethod.id != payment_id
        ).update({"is_default": False})
    
    payment_method.details = payment_data.details
    payment_method.is_default = payment_data.is_default
    db.commit()
    db.refresh(payment_method)
    return payment_method


def delete_payment_method(db: Session, payment_id: int, current_user: User) -> bool:
    payment_method = get_payment_method_by_id(db, payment_id, current_user)
    if not payment_method:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payment method not found"
        )
    
    db.delete(payment_method)
    db.commit()
    return True
