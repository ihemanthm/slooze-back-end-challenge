from enum import Enum
from fastapi import HTTPException, status


class UserRole(str, Enum):
    ADMIN = "ADMIN"
    MANAGER = "MANAGER"
    MEMBER = "MEMBER"


class Country(str, Enum):
    INDIA = "INDIA"
    AMERICA = "AMERICA"


class Permission:
    VIEW_RESTAURANTS = "view_restaurants"
    CREATE_ORDER = "create_order"
    CHECKOUT_ORDER = "checkout_order"
    CANCEL_ORDER = "cancel_order"
    MANAGE_PAYMENT_METHODS = "manage_payment_methods"


ROLE_PERMISSIONS = {
    UserRole.ADMIN: [
        Permission.VIEW_RESTAURANTS,
        Permission.CREATE_ORDER,
        Permission.CHECKOUT_ORDER,
        Permission.CANCEL_ORDER,
        Permission.MANAGE_PAYMENT_METHODS,
    ],
    UserRole.MANAGER: [
        Permission.VIEW_RESTAURANTS,
        Permission.CREATE_ORDER,
        Permission.CHECKOUT_ORDER,
        Permission.CANCEL_ORDER,
    ],
    UserRole.MEMBER: [
        Permission.VIEW_RESTAURANTS,
        Permission.CREATE_ORDER,
    ],
}


def check_permission(user_role: UserRole, permission: str) -> bool:
    return permission in ROLE_PERMISSIONS.get(user_role, [])


def require_permission(permission: str):
    def decorator(user_role: UserRole):
        if not check_permission(user_role, permission):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Permission denied. Required permission: {permission}"
            )
    return decorator


def can_access_country_data(user_role: UserRole, user_country: Country, data_country: Country) -> bool:
    if user_role == UserRole.ADMIN:
        return True
    return user_country == data_country
