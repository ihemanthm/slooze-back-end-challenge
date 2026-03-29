import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from app.main import app
from app.db.base import Base
from app.db.session import get_db
from app.core.security import get_password_hash
from app.models.user import User
from app.models.restaurant import Restaurant, MenuItem
from app.core.permissions import UserRole, Country

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db):
    def override_get_db():
        try:
            yield db
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def admin_user(db):
    user = User(
        email="admin@test.com",
        hashed_password=get_password_hash("admin123"),
        full_name="Admin User",
        role=UserRole.ADMIN,
        country=Country.AMERICA
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture
def manager_india(db):
    user = User(
        email="manager.india@test.com",
        hashed_password=get_password_hash("manager123"),
        full_name="Manager India",
        role=UserRole.MANAGER,
        country=Country.INDIA
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture
def member_america(db):
    user = User(
        email="member.america@test.com",
        hashed_password=get_password_hash("member123"),
        full_name="Member America",
        role=UserRole.MEMBER,
        country=Country.AMERICA
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture
def restaurant_india(db):
    restaurant = Restaurant(
        name="Test Restaurant India",
        description="Test description",
        cuisine_type="Indian",
        country=Country.INDIA,
        rating=4.5
    )
    db.add(restaurant)
    db.commit()
    db.refresh(restaurant)
    
    menu_item = MenuItem(
        restaurant_id=restaurant.id,
        name="Test Item",
        description="Test item description",
        price=100.0,
        category="Main Course"
    )
    db.add(menu_item)
    db.commit()
    
    return restaurant


@pytest.fixture
def restaurant_america(db):
    restaurant = Restaurant(
        name="Test Restaurant America",
        description="Test description",
        cuisine_type="American",
        country=Country.AMERICA,
        rating=4.5
    )
    db.add(restaurant)
    db.commit()
    db.refresh(restaurant)
    
    menu_item = MenuItem(
        restaurant_id=restaurant.id,
        name="Test Burger",
        description="Test burger description",
        price=10.0,
        category="Burgers"
    )
    db.add(menu_item)
    db.commit()
    
    return restaurant


def get_auth_token(client, email, password):
    response = client.post(
        "/api/v1/auth/login",
        data={"username": email, "password": password}
    )
    return response.json()["access_token"]
