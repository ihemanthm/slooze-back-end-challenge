from sqlalchemy.orm import Session
from app.models.restaurant import Restaurant, MenuItem
from app.models.user import User
from app.core.permissions import UserRole, can_access_country_data
from typing import List


def get_restaurants(db: Session, current_user: User) -> List[Restaurant]:
    query = db.query(Restaurant).filter(Restaurant.is_active == True)
    
    if current_user.role != UserRole.ADMIN:
        query = query.filter(Restaurant.country == current_user.country)
    
    return query.all()


def get_restaurant_by_id(db: Session, restaurant_id: int, current_user: User) -> Restaurant | None:
    restaurant = db.query(Restaurant).filter(
        Restaurant.id == restaurant_id,
        Restaurant.is_active == True
    ).first()
    
    if restaurant and current_user.role != UserRole.ADMIN:
        if not can_access_country_data(current_user.role, current_user.country, restaurant.country):
            return None
    
    return restaurant


def get_menu_items(db: Session, restaurant_id: int, current_user: User) -> List[MenuItem]:
    restaurant = get_restaurant_by_id(db, restaurant_id, current_user)
    if not restaurant:
        return []
    
    return db.query(MenuItem).filter(
        MenuItem.restaurant_id == restaurant_id,
        MenuItem.is_available == True
    ).all()
