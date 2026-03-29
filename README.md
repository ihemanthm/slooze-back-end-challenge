![Logo](./public/FFFFFF-1.png)
# Slooze Food Ordering Backend API

**ROLE:** **Software Engineer - Backend**

A production-ready role-based food ordering backend API built with FastAPI, implementing RBAC (Role-Based Access Control) and Re-BAC (Relationship-Based Access Control) for country-based data isolation.

## 🌐 Live Deployment

**The application is deployed and live on Render:**

🔗 **API Base URL:** https://slooze-back-end-challenge.onrender.com

📚 **Interactive API Documentation (Swagger UI):** https://slooze-back-end-challenge.onrender.com/docs

📖 **Alternative Documentation (ReDoc):** https://slooze-back-end-challenge.onrender.com/redoc

⚠️ **Note:** The free tier sleeps after 15 minutes of inactivity. First request may take ~30 seconds to wake up.

## ✨ Features Implemented

✅ **RBAC (8 points)** - Role-based permissions for Admin, Manager, and Member  
✅ **Re-BAC (10 bonus points)** - Country-based data isolation (India/America)  
✅ **Full Application (12 points)** - Complete food ordering system with all features  
✅ **Comprehensive Testing** - Automated test suite with pytest  
✅ **API Documentation** - Auto-generated Swagger UI and ReDoc  
✅ **Database Seeding** - Pre-populated with 6 users, 10 restaurants, 50+ menu items

## 🎯 Feature Breakdown & Role-Based Access

| **Feature**                      | **Admin** | **Manager** | **Member** |
|----------------------------------|----------|------------|------------|
| View restaurants & menu items   | ✅       | ✅         | ✅         |
| Create an order (add food items)| ✅       | ✅         | ✅         |
| Checkout & pay                  | ✅       | ✅         | ❌         |
| Cancel an order                 | ✅       | ✅         | ❌         |
| Add / Modify payment methods    | ✅       | ❌         | ❌         |

### Country-Based Access (Re-BAC)
- **Managers & Members**: Can only access data from their assigned country
- **Admin**: Has global access across all countries (India and America)

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- PostgreSQL 14+ (or use Docker)
- pip

### Installation

```bash
# 1. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Start PostgreSQL (using Docker)
docker-compose up -d

# 4. Setup environment
cp .env.example .env

# 5. Run migrations
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head

# 6. Seed database
python scripts/seed_data.py

# 7. Start server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Access Points
- **API**: http://localhost:8000
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔐 Test Credentials

| User | Email | Password | Role | Country |
|------|-------|----------|------|---------|
| Nick Fury | nick.fury@slooze.com | admin123 | ADMIN | AMERICA |
| Captain Marvel | captain.marvel@slooze.com | manager123 | MANAGER | INDIA |
| Captain America | captain.america@slooze.com | manager123 | MANAGER | AMERICA |
| Thanos | thanos@slooze.com | member123 | MEMBER | INDIA |
| Thor | thor@slooze.com | member123 | MEMBER | INDIA |
| Travis | travis@slooze.com | member123 | MEMBER | AMERICA |

## 📚 API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login and get JWT token
- `GET /api/v1/auth/me` - Get current user info

### Restaurants
- `GET /api/v1/restaurants` - List restaurants (country-filtered)
- `GET /api/v1/restaurants/{id}` - Get restaurant with menu
- `GET /api/v1/restaurants/{id}/menu` - Get menu items

### Orders
- `POST /api/v1/orders` - Create order
- `GET /api/v1/orders` - List user's orders
- `GET /api/v1/orders/{id}` - Get order details
- `POST /api/v1/orders/{id}/items` - Add items to order
- `POST /api/v1/orders/{id}/checkout` - Checkout (Admin/Manager only)
- `DELETE /api/v1/orders/{id}` - Cancel order (Admin/Manager only)

### Payment Methods
- `GET /api/v1/payment-methods` - List payment methods
- `POST /api/v1/payment-methods` - Add payment method (Admin only)
- `PUT /api/v1/payment-methods/{id}` - Update payment method (Admin only)
- `DELETE /api/v1/payment-methods/{id}` - Delete payment method (Admin only)

### 📥 Postman Collection

Download the OpenAPI specification for use with Postman or Insomnia:

**Option 1: From Live API**
```bash
curl https://slooze-back-end-challenge.onrender.com/api/v1/openapi.json > slooze-api.json
```

**Option 2: From Repository**
The `slooze-api-spec.json` file is included in the repository.

**Import to Postman:**
1. Open Postman → Import
2. Select the JSON file
3. All endpoints will be imported with examples

## 🧪 Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test
pytest tests/test_auth.py -v
```

## 🏗️ Tech Stack

- **Framework**: FastAPI 0.109.0
- **ORM**: SQLAlchemy 2.0.25
- **Database**: PostgreSQL 15
- **Authentication**: JWT (python-jose)
- **Password Hashing**: bcrypt
- **Migrations**: Alembic 1.13.1
- **Testing**: pytest 7.4.4
- **Validation**: Pydantic v2

## 📖 Documentation

### Complete Implementation Guide
**[Implementation.md](./Implementation.md)** - Comprehensive documentation including:
- Project architecture and design decisions
- Database schema and relationships
- RBAC and Re-BAC implementation details
- Complete setup instructions from scratch
- API usage examples with curl commands
- Security features and best practices
- Deployment considerations

### API Documentation
- **Live Swagger UI**: https://slooze-back-end-challenge.onrender.com/docs
- **Live ReDoc**: https://slooze-back-end-challenge.onrender.com/redoc
- **Local Swagger UI**: http://localhost:8000/docs (after starting server locally)
- **OpenAPI Spec**: Available in `slooze-api-spec.json`

### Additional Guides
- **[TESTING_GUIDE.md](./TESTING_GUIDE.md)** - How to test the application
- **[QUICK_START.md](./QUICK_START.md)** - Fast reference guide
- **[DEPLOYMENT.md](./DEPLOYMENT.md)** - Docker deployment instructions
- **[CLOUD_DEPLOYMENT.md](./CLOUD_DEPLOYMENT.md)** - Cloud platform deployment (Render, Railway, Fly.io)

## 🎯 Project Structure

```
slooze-backend-challenge/
├── app/
│   ├── api/v1/          # API endpoints
│   ├── core/            # Config, security, permissions
│   ├── models/          # SQLAlchemy models
│   ├── schemas/         # Pydantic schemas
│   ├── services/        # Business logic
│   └── db/              # Database session
├── alembic/             # Database migrations
├── scripts/             # Utility scripts
├── tests/               # Test suite
└── Implementation.md    # Detailed documentation
```

## 🔒 Security Features

- JWT-based authentication with token expiration
- Password hashing with bcrypt
- Role and country claims in JWT payload
- Input validation with Pydantic
- SQL injection prevention via ORM
- CORS configuration