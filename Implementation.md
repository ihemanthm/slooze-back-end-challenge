# Slooze Food Ordering Backend - Implementation Documentation

## 📋 Project Overview

This is a **role-based food ordering backend API** built with FastAPI that implements:
- **RBAC (Role-Based Access Control)**
- **Re-BAC (Relationship-Based Access Control)**
- **Full-featured food ordering system**

## 🏗️ Architecture

### Technology Stack
- **Framework**: FastAPI 0.109.0 (async, auto-documented)
- **ORM**: SQLAlchemy 2.0.25
- **Database**: PostgreSQL 15
- **Authentication**: JWT (python-jose)
- **Password Hashing**: bcrypt (passlib)
- **Migrations**: Alembic 1.13.1
- **Testing**: pytest 7.4.4

### Project Structure
```
slooze-backend-challenge/
├── app/
│   ├── api/
│   │   ├── deps.py              # Auth dependencies & role checkers
│   │   └── v1/
│   │       ├── auth.py          # Authentication endpoints
│   │       ├── restaurants.py   # Restaurant & menu endpoints
│   │       ├── orders.py        # Order management endpoints
│   │       └── payments.py      # Payment method endpoints
│   ├── core/
│   │   ├── config.py            # Settings & environment config
│   │   ├── security.py          # JWT & password utilities
│   │   └── permissions.py       # RBAC & Re-BAC logic
│   ├── models/
│   │   ├── user.py              # User model
│   │   ├── restaurant.py        # Restaurant & MenuItem models
│   │   ├── order.py             # Order & OrderItem models
│   │   └── payment.py           # PaymentMethod model
│   ├── schemas/
│   │   ├── user.py              # Pydantic schemas for users
│   │   ├── restaurant.py        # Pydantic schemas for restaurants
│   │   ├── order.py             # Pydantic schemas for orders
│   │   └── payment.py           # Pydantic schemas for payments
│   ├── services/
│   │   ├── auth_service.py      # Authentication business logic
│   │   ├── restaurant_service.py # Restaurant business logic
│   │   ├── order_service.py     # Order business logic
│   │   └── payment_service.py   # Payment business logic
│   ├── db/
│   │   ├── base.py              # SQLAlchemy base
│   │   └── session.py           # Database session
│   └── main.py                  # FastAPI application
├── alembic/                     # Database migrations
├── scripts/
│   └── seed_data.py             # Database seeding script
├── tests/                       # Test suite
├── docker-compose.yml           # PostgreSQL container
├── requirements.txt             # Python dependencies
└── Implementation.md            # This file
```

## 🎯 Features Implemented

### 1. Role-Based Access Control (RBAC) - 8 Points ✅

**Three Roles with Distinct Permissions:**

| Feature | Admin | Manager | Member |
|---------|-------|---------|--------|
| View restaurants & menu items | ✅ | ✅ | ✅ |
| Create order (add food items) | ✅ | ✅ | ✅ |
| Checkout & pay | ✅ | ✅ | ❌ |
| Cancel order | ✅ | ✅ | ❌ |
| Add/Modify payment methods | ✅ | ❌ | ❌ |

**Implementation Details:**
- `RoleChecker` dependency in `app/api/deps.py` enforces role requirements
- Permission matrix defined in `app/core/permissions.py`
- Decorators applied to endpoints: `Depends(RoleChecker([UserRole.ADMIN, UserRole.MANAGER]))`

### 2. Relationship-Based Access Control (Re-BAC) - 10 Bonus Points ✅

**Country-Based Data Isolation:**
- **Managers & Members**: Can only access data from their assigned country (India or America)
- **Admin**: Has global access across all countries

**Implementation:**
- Country filtering at service layer in all restaurant and order queries
- `can_access_country_data()` function validates access rights
- Orders automatically inherit country from restaurant
- Prevents cross-country data leakage

**Example:**
- Manager India can only see Indian restaurants and orders
- Manager America cannot access Indian data
- Admin sees everything

### 3. Full-Featured Food Ordering System - 12 Points ✅

**Authentication APIs:**
- `POST /api/v1/auth/register` - User registration
- `POST /api/v1/auth/login` - JWT token generation
- `GET /api/v1/auth/me` - Get current user info

**Restaurant & Menu APIs:**
- `GET /api/v1/restaurants` - List restaurants (country-filtered)
- `GET /api/v1/restaurants/{id}` - Get restaurant details with menu
- `GET /api/v1/restaurants/{id}/menu` - Get menu items

**Order Management APIs:**
- `POST /api/v1/orders` - Create order with items
- `GET /api/v1/orders` - List user's orders (country-filtered)
- `GET /api/v1/orders/{id}` - Get order details
- `POST /api/v1/orders/{id}/items` - Add items to existing order
- `POST /api/v1/orders/{id}/checkout` - Checkout & pay (Admin/Manager only)
- `DELETE /api/v1/orders/{id}` - Cancel order (Admin/Manager only)

**Payment Method APIs:**
- `GET /api/v1/payment-methods` - List payment methods
- `POST /api/v1/payment-methods` - Add payment method (Admin only)
- `PUT /api/v1/payment-methods/{id}` - Update payment method (Admin only)
- `DELETE /api/v1/payment-methods/{id}` - Delete payment method (Admin only)

## 🗄️ Database Schema

### Users Table
- Stores user credentials, role, and country assignment
- Password hashing with bcrypt
- Enum fields for role (ADMIN/MANAGER/MEMBER) and country (INDIA/AMERICA)

### Restaurants Table
- Restaurant information with country assignment
- Supports rating and active status
- One-to-many relationship with menu items

### MenuItems Table
- Food items belonging to restaurants
- Price, category, availability status
- Foreign key to restaurants

### Orders Table
- User orders with status tracking (PENDING/CONFIRMED/CANCELLED)
- Country field inherited from restaurant
- Total amount calculation
- One-to-many relationship with order items

### OrderItems Table
- Individual items in an order
- Captures price at time of order (price history)
- Quantity and subtotal

### PaymentMethods Table
- User payment methods (CREDIT_CARD/DEBIT_CARD/UPI/WALLET)
- Encrypted details field
- Default payment method flag

## 🚀 Setup Instructions

### Prerequisites
- Python 3.11 or higher
- PostgreSQL 14 or higher
- Docker (optional, for PostgreSQL)

### Step 1: Clone Repository
```bash
cd slooze-backend-challenge
```

### Step 2: Create Virtual Environment
```bash
python -m venv venv

# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Setup PostgreSQL Database

**Option A: Using Docker (Recommended)**
```bash
docker-compose up -d
```

**Option B: Manual PostgreSQL Setup**
```bash
# Create database
createdb slooze_db

# Create user
psql -c "CREATE USER slooze_user WITH PASSWORD 'slooze_pass';"
psql -c "GRANT ALL PRIVILEGES ON DATABASE slooze_db TO slooze_user;"
```

### Step 5: Configure Environment Variables
```bash
cp .env.example .env

# Edit .env file with your database credentials if needed
# Default values work with Docker setup
```

### Step 6: Run Database Migrations
```bash
# Initialize Alembic (first time only)
alembic revision --autogenerate -m "Initial migration"

# Apply migrations
alembic upgrade head
```

### Step 7: Seed Database
```bash
python scripts/seed_data.py
```

**Seeded Data:**
- 6 users (1 Admin, 2 Managers, 3 Members)
- 10 restaurants (5 India, 5 America)
- 50+ menu items
- 2 payment methods for Admin

### Step 8: Start Server
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Step 9: Access API Documentation
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **API Root**: http://localhost:8000

## 🔐 Test Credentials

| User | Email | Password | Role | Country |
|------|-------|----------|------|---------|
| Nick Fury | nick.fury@slooze.com | admin123 | ADMIN | AMERICA |
| Captain Marvel | captain.marvel@slooze.com | manager123 | MANAGER | INDIA |
| Captain America | captain.america@slooze.com | manager123 | MANAGER | AMERICA |
| Thanos | thanos@slooze.com | member123 | MEMBER | INDIA |
| Thor | thor@slooze.com | member123 | MEMBER | INDIA |
| Travis | travis@slooze.com | member123 | MEMBER | AMERICA |

## 🧪 Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_auth.py -v

# Run tests matching pattern
pytest -k "test_rbac" -v
```

**Test Coverage:**
- Authentication tests
- RBAC enforcement tests
- Re-BAC country-based access tests
- Order management tests

## 📝 API Usage Examples

### 1. Login
```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=nick.fury@slooze.com&password=admin123"
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### 2. List Restaurants (Country-Filtered)
```bash
curl -X GET "http://localhost:8000/api/v1/restaurants" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Response for Manager India:**
```json
[
  {
    "id": 1,
    "name": "Biryani House",
    "country": "INDIA",
    "cuisine_type": "Indian",
    "rating": 4.5
  }
]
```

### 3. Create Order
```bash
curl -X POST "http://localhost:8000/api/v1/orders" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "restaurant_id": 1,
    "items": [
      {"menu_item_id": 1, "quantity": 2},
      {"menu_item_id": 2, "quantity": 1}
    ]
  }'
```

### 4. Checkout Order (Manager/Admin Only)
```bash
curl -X POST "http://localhost:8000/api/v1/orders/1/checkout" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"payment_method_id": 1}'
```

## 🔒 Security Features

1. **Password Security**: bcrypt hashing with salt
2. **JWT Authentication**: Secure token-based auth with expiration
3. **Role Claims in JWT**: Role and country embedded in token payload
4. **Input Validation**: Pydantic models validate all requests
5. **SQL Injection Prevention**: SQLAlchemy ORM parameterized queries
6. **CORS Configuration**: Configurable cross-origin settings

## 🎨 Design Patterns

1. **Repository Pattern**: Service layer abstracts database operations
2. **Dependency Injection**: FastAPI's dependency system for auth & DB
3. **Factory Pattern**: Session management with context managers
4. **Decorator Pattern**: Role checking decorators for endpoints
5. **Strategy Pattern**: Different access strategies for roles

## 📊 Key Implementation Highlights

### RBAC Implementation
```python
# Role checker dependency
class RoleChecker:
    def __init__(self, allowed_roles: list[UserRole]):
        self.allowed_roles = allowed_roles
    
    def __call__(self, current_user: User = Depends(get_current_user)):
        if current_user.role not in self.allowed_roles:
            raise HTTPException(status_code=403, detail="Access denied")
        return current_user

# Usage in endpoint
@router.post("/{order_id}/checkout")
def checkout(
    order_id: int,
    current_user: User = Depends(RoleChecker([UserRole.ADMIN, UserRole.MANAGER]))
):
    ...
```

### Re-BAC Implementation
```python
def can_access_country_data(user_role, user_country, data_country):
    # Admin has global access
    if user_role == UserRole.ADMIN:
        return True
    # Others restricted to their country
    return user_country == data_country

# Applied in service layer
def get_restaurants(db: Session, current_user: User):
    query = db.query(Restaurant).filter(Restaurant.is_active)
    
    if current_user.role != UserRole.ADMIN:
        query = query.filter(Restaurant.country == current_user.country)
    
    return query.all()
```

## 🚢 Deployment Considerations

### Environment Variables
- `DATABASE_URL`: PostgreSQL connection string
- `SECRET_KEY`: JWT signing key (change in production!)
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiration time

### Production Checklist
- [ ] Change `SECRET_KEY` to a secure random value
- [ ] Use environment-specific database credentials
- [ ] Enable HTTPS/TLS
- [ ] Configure proper CORS origins
- [ ] Set up database backups
- [ ] Implement rate limiting
- [ ] Add logging and monitoring
- [ ] Use production WSGI server (gunicorn + uvicorn workers)

## 📚 API Documentation

The API is fully documented with OpenAPI 3.0 specification:
- Interactive documentation at `/docs` (Swagger UI)
- Alternative documentation at `/redoc` (ReDoc)
- OpenAPI JSON schema at `/api/v1/openapi.json`

## 🎯 Success Criteria Met

✅ **RBAC**: Fully implemented with role-based permissions  
✅ **Re-BAC**: Country-based data isolation for Managers/Members  
✅ **Full Application**: All features working with proper API endpoints  
✅ **Documentation**: Comprehensive setup instructions and API docs  
✅ **Testing**: Automated test suite with pytest  
✅ **Seed Data**: 6 users, 10+ restaurants, 50+ menu items  
✅ **Clean Architecture**: Modular, maintainable, production-ready code