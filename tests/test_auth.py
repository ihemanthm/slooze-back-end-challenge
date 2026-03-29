from fastapi import status


def test_register_user(client):
    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "newuser@test.com",
            "password": "password123",
            "full_name": "New User",
            "role": "MEMBER",
            "country": "INDIA"
        }
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["email"] == "newuser@test.com"
    assert data["full_name"] == "New User"
    assert data["role"] == "MEMBER"


def test_register_duplicate_email(client, admin_user):
    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "admin@test.com",
            "password": "password123",
            "full_name": "Duplicate User",
            "role": "MEMBER",
            "country": "INDIA"
        }
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_login_success(client, admin_user):
    response = client.post(
        "/api/v1/auth/login",
        data={"username": "admin@test.com", "password": "admin123"}
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_invalid_credentials(client, admin_user):
    response = client.post(
        "/api/v1/auth/login",
        data={"username": "admin@test.com", "password": "wrongpassword"}
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_get_current_user(client, admin_user):
    from tests.conftest import get_auth_token
    
    token = get_auth_token(client, "admin@test.com", "admin123")
    response = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["email"] == "admin@test.com"
    assert data["role"] == "ADMIN"
