from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.schemas.restaurant import Restaurant, RestaurantWithMenu, MenuItem
from app.services.restaurant_service import get_restaurants, get_restaurant_by_id, get_menu_items
from app.api.deps import get_current_user
from app.models.user import User

router = APIRouter()


@router.get("/", response_model=List[Restaurant])
def list_restaurants(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_restaurants(db, current_user)


@router.get("/{restaurant_id}", response_model=RestaurantWithMenu)
def get_restaurant(
    restaurant_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    restaurant = get_restaurant_by_id(db, restaurant_id, current_user)
    if not restaurant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Restaurant not found"
        )
    return restaurant


@router.get("/{restaurant_id}/menu", response_model=List[MenuItem])
def get_restaurant_menu(
    restaurant_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    menu_items = get_menu_items(db, restaurant_id, current_user)
    if not menu_items:
        restaurant = get_restaurant_by_id(db, restaurant_id, current_user)
        if not restaurant:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Restaurant not found"
            )
    return menu_items
