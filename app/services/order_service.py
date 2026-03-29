from sqlalchemy.orm import Session
from app.models.order import Order, OrderItem, OrderStatus
from app.models.restaurant import MenuItem
from app.models.user import User
from app.schemas.order import OrderCreate, OrderItemCreate
from app.core.permissions import UserRole, can_access_country_data
from fastapi import HTTPException, status
from typing import List


def create_order(db: Session, order_data: OrderCreate, current_user: User) -> Order:
    from app.services.restaurant_service import get_restaurant_by_id
    
    restaurant = get_restaurant_by_id(db, order_data.restaurant_id, current_user)
    if not restaurant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Restaurant not found or not accessible"
        )
    
    order = Order(
        user_id=current_user.id,
        restaurant_id=order_data.restaurant_id,
        country=restaurant.country,
        status=OrderStatus.PENDING
    )
    db.add(order)
    db.flush()
    
    total_amount = 0.0
    for item in order_data.items:
        menu_item = db.query(MenuItem).filter(
            MenuItem.id == item.menu_item_id,
            MenuItem.restaurant_id == order_data.restaurant_id,
            MenuItem.is_available == True
        ).first()
        
        if not menu_item:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Menu item {item.menu_item_id} not found or not available"
            )
        
        subtotal = menu_item.price * item.quantity
        total_amount += subtotal
        
        order_item = OrderItem(
            order_id=order.id,
            menu_item_id=item.menu_item_id,
            quantity=item.quantity,
            price_at_order=menu_item.price,
            subtotal=subtotal
        )
        db.add(order_item)
    
    order.total_amount = total_amount
    db.commit()
    db.refresh(order)
    return order


def get_user_orders(db: Session, current_user: User) -> List[Order]:
    query = db.query(Order).filter(Order.user_id == current_user.id)
    
    if current_user.role != UserRole.ADMIN:
        query = query.filter(Order.country == current_user.country)
    
    return query.all()


def get_order_by_id(db: Session, order_id: int, current_user: User) -> Order | None:
    order = db.query(Order).filter(Order.id == order_id).first()
    
    if not order:
        return None
    
    if order.user_id != current_user.id and current_user.role != UserRole.ADMIN:
        return None
    
    if current_user.role != UserRole.ADMIN:
        if not can_access_country_data(current_user.role, current_user.country, order.country):
            return None
    
    return order


def checkout_order(db: Session, order_id: int, payment_method_id: int, current_user: User) -> Order:
    order = get_order_by_id(db, order_id, current_user)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    
    if order.status != OrderStatus.PENDING:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Order is not in pending status"
        )
    
    order.status = OrderStatus.CONFIRMED
    db.commit()
    db.refresh(order)
    return order


def cancel_order(db: Session, order_id: int, current_user: User) -> Order:
    order = get_order_by_id(db, order_id, current_user)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    
    if order.status == OrderStatus.CANCELLED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Order is already cancelled"
        )
    
    order.status = OrderStatus.CANCELLED
    db.commit()
    db.refresh(order)
    return order


def add_items_to_order(db: Session, order_id: int, items: List[OrderItemCreate], current_user: User) -> Order:
    order = get_order_by_id(db, order_id, current_user)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    
    if order.status != OrderStatus.PENDING:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot add items to non-pending order"
        )
    
    for item in items:
        menu_item = db.query(MenuItem).filter(
            MenuItem.id == item.menu_item_id,
            MenuItem.restaurant_id == order.restaurant_id,
            MenuItem.is_available == True
        ).first()
        
        if not menu_item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Menu item {item.menu_item_id} not found or not available"
            )
        
        subtotal = menu_item.price * item.quantity
        order.total_amount += subtotal
        
        order_item = OrderItem(
            order_id=order.id,
            menu_item_id=item.menu_item_id,
            quantity=item.quantity,
            price_at_order=menu_item.price,
            subtotal=subtotal
        )
        db.add(order_item)
    
    db.commit()
    db.refresh(order)
    return order
