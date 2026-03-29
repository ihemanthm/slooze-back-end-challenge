import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.user import User
from app.models.restaurant import Restaurant, MenuItem
from app.models.payment import PaymentMethod, PaymentMethodType
from app.core.permissions import UserRole, Country
from app.core.security import get_password_hash


def seed_users(db: Session):
    users_data = [
        {
            "email": "nick.fury@slooze.com",
            "password": "admin123",
            "full_name": "Nick Fury",
            "role": UserRole.ADMIN,
            "country": Country.AMERICA
        },
        {
            "email": "captain.marvel@slooze.com",
            "password": "manager123",
            "full_name": "Captain Marvel",
            "role": UserRole.MANAGER,
            "country": Country.INDIA
        },
        {
            "email": "captain.america@slooze.com",
            "password": "manager123",
            "full_name": "Captain America",
            "role": UserRole.MANAGER,
            "country": Country.AMERICA
        },
        {
            "email": "thanos@slooze.com",
            "password": "member123",
            "full_name": "Thanos",
            "role": UserRole.MEMBER,
            "country": Country.INDIA
        },
        {
            "email": "thor@slooze.com",
            "password": "member123",
            "full_name": "Thor",
            "role": UserRole.MEMBER,
            "country": Country.INDIA
        },
        {
            "email": "travis@slooze.com",
            "password": "member123",
            "full_name": "Travis",
            "role": UserRole.MEMBER,
            "country": Country.AMERICA
        }
    ]
    
    for user_data in users_data:
        existing_user = db.query(User).filter(User.email == user_data["email"]).first()
        if not existing_user:
            user = User(
                email=user_data["email"],
                hashed_password=get_password_hash(user_data["password"]),
                full_name=user_data["full_name"],
                role=user_data["role"],
                country=user_data["country"]
            )
            db.add(user)
    
    db.commit()
    print("✅ Users seeded successfully")


def seed_restaurants(db: Session):
    restaurants_data = [
        {
            "name": "Biryani House",
            "description": "Authentic Hyderabadi Biryani and Indian cuisine",
            "cuisine_type": "Indian",
            "country": Country.INDIA,
            "rating": 4.5
        },
        {
            "name": "Dosa Corner",
            "description": "South Indian delicacies and crispy dosas",
            "cuisine_type": "South Indian",
            "country": Country.INDIA,
            "rating": 4.3
        },
        {
            "name": "Tandoor Palace",
            "description": "North Indian tandoori specialties",
            "cuisine_type": "North Indian",
            "country": Country.INDIA,
            "rating": 4.6
        },
        {
            "name": "Mumbai Chaat House",
            "description": "Street food and chaat items",
            "cuisine_type": "Street Food",
            "country": Country.INDIA,
            "rating": 4.2
        },
        {
            "name": "Curry Kingdom",
            "description": "Variety of Indian curries and breads",
            "cuisine_type": "Indian",
            "country": Country.INDIA,
            "rating": 4.4
        },
        {
            "name": "Burger King",
            "description": "Flame-grilled burgers and fries",
            "cuisine_type": "American",
            "country": Country.AMERICA,
            "rating": 4.1
        },
        {
            "name": "Pizza Hub",
            "description": "Wood-fired pizzas and Italian cuisine",
            "cuisine_type": "Italian",
            "country": Country.AMERICA,
            "rating": 4.5
        },
        {
            "name": "Taco Bell",
            "description": "Mexican-inspired fast food",
            "cuisine_type": "Mexican",
            "country": Country.AMERICA,
            "rating": 4.0
        },
        {
            "name": "Steakhouse Grill",
            "description": "Premium steaks and grilled meats",
            "cuisine_type": "Steakhouse",
            "country": Country.AMERICA,
            "rating": 4.7
        },
        {
            "name": "Seafood Shack",
            "description": "Fresh seafood and coastal cuisine",
            "cuisine_type": "Seafood",
            "country": Country.AMERICA,
            "rating": 4.4
        }
    ]
    
    for rest_data in restaurants_data:
        existing = db.query(Restaurant).filter(
            Restaurant.name == rest_data["name"],
            Restaurant.country == rest_data["country"]
        ).first()
        if not existing:
            restaurant = Restaurant(**rest_data)
            db.add(restaurant)
    
    db.commit()
    print("✅ Restaurants seeded successfully")


def seed_menu_items(db: Session):
    menu_items_data = [
        {"restaurant": "Biryani House", "name": "Chicken Biryani", "price": 299.0, "category": "Main Course"},
        {"restaurant": "Biryani House", "name": "Mutton Biryani", "price": 349.0, "category": "Main Course"},
        {"restaurant": "Biryani House", "name": "Veg Biryani", "price": 249.0, "category": "Main Course"},
        {"restaurant": "Biryani House", "name": "Raita", "price": 49.0, "category": "Sides"},
        {"restaurant": "Biryani House", "name": "Gulab Jamun", "price": 79.0, "category": "Dessert"},
        
        {"restaurant": "Dosa Corner", "name": "Masala Dosa", "price": 120.0, "category": "Main Course"},
        {"restaurant": "Dosa Corner", "name": "Onion Dosa", "price": 110.0, "category": "Main Course"},
        {"restaurant": "Dosa Corner", "name": "Idli Sambar", "price": 80.0, "category": "Breakfast"},
        {"restaurant": "Dosa Corner", "name": "Vada", "price": 60.0, "category": "Snacks"},
        {"restaurant": "Dosa Corner", "name": "Filter Coffee", "price": 40.0, "category": "Beverages"},
        
        {"restaurant": "Tandoor Palace", "name": "Tandoori Chicken", "price": 399.0, "category": "Main Course"},
        {"restaurant": "Tandoor Palace", "name": "Paneer Tikka", "price": 299.0, "category": "Appetizers"},
        {"restaurant": "Tandoor Palace", "name": "Butter Naan", "price": 45.0, "category": "Breads"},
        {"restaurant": "Tandoor Palace", "name": "Dal Makhani", "price": 199.0, "category": "Main Course"},
        {"restaurant": "Tandoor Palace", "name": "Lassi", "price": 70.0, "category": "Beverages"},
        
        {"restaurant": "Mumbai Chaat House", "name": "Pani Puri", "price": 60.0, "category": "Chaat"},
        {"restaurant": "Mumbai Chaat House", "name": "Bhel Puri", "price": 70.0, "category": "Chaat"},
        {"restaurant": "Mumbai Chaat House", "name": "Pav Bhaji", "price": 120.0, "category": "Main Course"},
        {"restaurant": "Mumbai Chaat House", "name": "Vada Pav", "price": 40.0, "category": "Snacks"},
        {"restaurant": "Mumbai Chaat House", "name": "Cutting Chai", "price": 20.0, "category": "Beverages"},
        
        {"restaurant": "Curry Kingdom", "name": "Chicken Curry", "price": 279.0, "category": "Main Course"},
        {"restaurant": "Curry Kingdom", "name": "Palak Paneer", "price": 229.0, "category": "Main Course"},
        {"restaurant": "Curry Kingdom", "name": "Roti", "price": 25.0, "category": "Breads"},
        {"restaurant": "Curry Kingdom", "name": "Jeera Rice", "price": 120.0, "category": "Rice"},
        {"restaurant": "Curry Kingdom", "name": "Mango Lassi", "price": 80.0, "category": "Beverages"},
        
        {"restaurant": "Burger King", "name": "Whopper", "price": 8.99, "category": "Burgers"},
        {"restaurant": "Burger King", "name": "Chicken Royale", "price": 7.99, "category": "Burgers"},
        {"restaurant": "Burger King", "name": "Veggie Burger", "price": 6.99, "category": "Burgers"},
        {"restaurant": "Burger King", "name": "French Fries", "price": 3.49, "category": "Sides"},
        {"restaurant": "Burger King", "name": "Coca Cola", "price": 2.49, "category": "Beverages"},
        
        {"restaurant": "Pizza Hub", "name": "Margherita Pizza", "price": 12.99, "category": "Pizza"},
        {"restaurant": "Pizza Hub", "name": "Pepperoni Pizza", "price": 14.99, "category": "Pizza"},
        {"restaurant": "Pizza Hub", "name": "BBQ Chicken Pizza", "price": 15.99, "category": "Pizza"},
        {"restaurant": "Pizza Hub", "name": "Garlic Bread", "price": 5.99, "category": "Sides"},
        {"restaurant": "Pizza Hub", "name": "Tiramisu", "price": 6.99, "category": "Dessert"},
        
        {"restaurant": "Taco Bell", "name": "Crunchy Taco", "price": 3.99, "category": "Tacos"},
        {"restaurant": "Taco Bell", "name": "Burrito Supreme", "price": 7.99, "category": "Burritos"},
        {"restaurant": "Taco Bell", "name": "Quesadilla", "price": 6.99, "category": "Quesadillas"},
        {"restaurant": "Taco Bell", "name": "Nachos", "price": 5.99, "category": "Sides"},
        {"restaurant": "Taco Bell", "name": "Mountain Dew", "price": 2.49, "category": "Beverages"},
        
        {"restaurant": "Steakhouse Grill", "name": "Ribeye Steak", "price": 34.99, "category": "Steaks"},
        {"restaurant": "Steakhouse Grill", "name": "Filet Mignon", "price": 39.99, "category": "Steaks"},
        {"restaurant": "Steakhouse Grill", "name": "Grilled Salmon", "price": 28.99, "category": "Seafood"},
        {"restaurant": "Steakhouse Grill", "name": "Mashed Potatoes", "price": 6.99, "category": "Sides"},
        {"restaurant": "Steakhouse Grill", "name": "Red Wine", "price": 12.99, "category": "Beverages"},
        
        {"restaurant": "Seafood Shack", "name": "Fish & Chips", "price": 16.99, "category": "Main Course"},
        {"restaurant": "Seafood Shack", "name": "Lobster Roll", "price": 24.99, "category": "Main Course"},
        {"restaurant": "Seafood Shack", "name": "Shrimp Scampi", "price": 22.99, "category": "Main Course"},
        {"restaurant": "Seafood Shack", "name": "Clam Chowder", "price": 8.99, "category": "Soups"},
        {"restaurant": "Seafood Shack", "name": "Iced Tea", "price": 2.99, "category": "Beverages"}
    ]
    
    for item_data in menu_items_data:
        restaurant = db.query(Restaurant).filter(Restaurant.name == item_data["restaurant"]).first()
        if restaurant:
            existing = db.query(MenuItem).filter(
                MenuItem.restaurant_id == restaurant.id,
                MenuItem.name == item_data["name"]
            ).first()
            if not existing:
                menu_item = MenuItem(
                    restaurant_id=restaurant.id,
                    name=item_data["name"],
                    description=f"Delicious {item_data['name']}",
                    price=item_data["price"],
                    category=item_data["category"]
                )
                db.add(menu_item)
    
    db.commit()
    print("✅ Menu items seeded successfully")


def seed_payment_methods(db: Session):
    admin_user = db.query(User).filter(User.email == "nick.fury@slooze.com").first()
    if admin_user:
        existing = db.query(PaymentMethod).filter(PaymentMethod.user_id == admin_user.id).first()
        if not existing:
            payment_methods = [
                PaymentMethod(
                    user_id=admin_user.id,
                    method_type=PaymentMethodType.CREDIT_CARD,
                    details="Visa ending in 1234",
                    is_default=True
                ),
                PaymentMethod(
                    user_id=admin_user.id,
                    method_type=PaymentMethodType.UPI,
                    details="nick.fury@upi",
                    is_default=False
                )
            ]
            for pm in payment_methods:
                db.add(pm)
            db.commit()
            print("✅ Payment methods seeded successfully")


def main():
    print("🌱 Starting database seeding...")
    db = SessionLocal()
    try:
        seed_users(db)
        seed_restaurants(db)
        seed_menu_items(db)
        seed_payment_methods(db)
        print("\n✨ Database seeding completed successfully!")
        print("\n📝 Seeded Data Summary:")
        print(f"   - Users: {db.query(User).count()}")
        print(f"   - Restaurants: {db.query(Restaurant).count()}")
        print(f"   - Menu Items: {db.query(MenuItem).count()}")
        print(f"   - Payment Methods: {db.query(PaymentMethod).count()}")
        print("\n🔐 Test Credentials:")
        print("   Admin: nick.fury@slooze.com / admin123")
        print("   Manager (India): captain.marvel@slooze.com / manager123")
        print("   Manager (America): captain.america@slooze.com / manager123")
        print("   Member (India): thanos@slooze.com / member123")
        print("   Member (India): thor@slooze.com / member123")
        print("   Member (America): travis@slooze.com / member123")
    except Exception as e:
        print(f"❌ Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    main()
