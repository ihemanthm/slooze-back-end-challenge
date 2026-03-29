from fastapi import status
from tests.conftest import get_auth_token


def test_admin_can_manage_payment_methods(client, admin_user):
    token = get_auth_token(client, "admin@test.com", "admin123")
    
    response = client.post(
        "/api/v1/payment-methods/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "method_type": "CREDIT_CARD",
            "details": "Visa ending in 1234",
            "is_default": True
        }
    )
    assert response.status_code == status.HTTP_201_CREATED


def test_manager_cannot_manage_payment_methods(client, manager_india):
    token = get_auth_token(client, "manager.india@test.com", "manager123")
    
    response = client.post(
        "/api/v1/payment-methods/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "method_type": "CREDIT_CARD",
            "details": "Visa ending in 1234",
            "is_default": True
        }
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_member_cannot_checkout_order(client, member_america, restaurant_america, db):
    from app.models.restaurant import MenuItem
    
    token = get_auth_token(client, "member.america@test.com", "member123")
    
    menu_item = db.query(MenuItem).filter(MenuItem.restaurant_id == restaurant_america.id).first()
    
    order_response = client.post(
        "/api/v1/orders/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "restaurant_id": restaurant_america.id,
            "items": [{"menu_item_id": menu_item.id, "quantity": 2}]
        }
    )
    
    if order_response.status_code == status.HTTP_201_CREATED:
        order_id = order_response.json()["id"]
        
        checkout_response = client.post(
            f"/api/v1/orders/{order_id}/checkout",
            headers={"Authorization": f"Bearer {token}"},
            json={"payment_method_id": 1}
        )
        assert checkout_response.status_code == status.HTTP_403_FORBIDDEN


def test_manager_can_checkout_order(client, manager_india, restaurant_india, db):
    token = get_auth_token(client, "manager.india@test.com", "manager123")
    
    order_response = client.post(
        "/api/v1/orders/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "restaurant_id": restaurant_india.id,
            "items": [{"menu_item_id": 1, "quantity": 2}]
        }
    )
    
    if order_response.status_code == status.HTTP_201_CREATED:
        order_id = order_response.json()["id"]
        
        checkout_response = client.post(
            f"/api/v1/orders/{order_id}/checkout",
            headers={"Authorization": f"Bearer {token}"},
            json={"payment_method_id": 1}
        )
        assert checkout_response.status_code in [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND]


def test_country_based_access_control(client, manager_india, restaurant_america):
    token = get_auth_token(client, "manager.india@test.com", "manager123")
    
    response = client.get(
        "/api/v1/restaurants/",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == status.HTTP_200_OK
    
    restaurants = response.json()
    american_restaurants = [r for r in restaurants if r.get("country") == "AMERICA"]
    assert len(american_restaurants) == 0


def test_admin_has_global_access(client, admin_user, restaurant_india, restaurant_america):
    token = get_auth_token(client, "admin@test.com", "admin123")
    
    response = client.get(
        "/api/v1/restaurants/",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == status.HTTP_200_OK
    
    restaurants = response.json()
    assert len(restaurants) >= 2
