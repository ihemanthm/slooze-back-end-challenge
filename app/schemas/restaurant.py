from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
from app.core.permissions import Country


class MenuItemBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    category: Optional[str] = None


class MenuItem(MenuItemBase):
    id: int
    restaurant_id: int
    is_available: bool
    created_at: datetime

    class Config:
        from_attributes = True


class RestaurantBase(BaseModel):
    name: str
    description: Optional[str] = None
    cuisine_type: Optional[str] = None
    country: Country


class Restaurant(RestaurantBase):
    id: int
    rating: float
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class RestaurantWithMenu(Restaurant):
    menu_items: List[MenuItem] = []

    class Config:
        from_attributes = True
