from pydantic import BaseModel
from datetime import datetime
from typing import List
from app.models.order import OrderStatus
from app.core.permissions import Country


class OrderItemCreate(BaseModel):
    menu_item_id: int
    quantity: int


class OrderItemResponse(BaseModel):
    id: int
    menu_item_id: int
    quantity: int
    price_at_order: float
    subtotal: float

    class Config:
        from_attributes = True


class OrderCreate(BaseModel):
    restaurant_id: int
    items: List[OrderItemCreate]


class OrderResponse(BaseModel):
    id: int
    user_id: int
    restaurant_id: int
    status: OrderStatus
    total_amount: float
    country: Country
    created_at: datetime
    updated_at: datetime
    order_items: List[OrderItemResponse] = []

    class Config:
        from_attributes = True


class OrderCheckout(BaseModel):
    payment_method_id: int
