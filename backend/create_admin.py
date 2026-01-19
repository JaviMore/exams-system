"""
Script para crear un usuario administrador inicial
"""
from app.core.database import SessionLocal
from app.models.user import User
from app.core.security import get_password_hash
import sys


def create_admin_user(email: str, password: str, full_name: str = "Administrator"):
    """Create an admin user"""
    db = SessionLocal()
    
    try:
        # Check if user already exists
        existing_user = db.query(User).filter(User.email == email).first()
        if existing_user:
            print(f"❌ User with email {email} already exists!")
            return False
        
        # Create admin user
        admin = User(
            email=email,
            hashed_password=get_password_hash(password),
            full_name=full_name,
            is_admin=True,
            is_active=True
        )
        
        db.add(admin)
        db.commit()
        db.refresh(admin)
        
        print(f"✅ Admin user created successfully!")
        print(f"   Email: {email}")
        print(f"   Name: {full_name}")
        print(f"   Password: {password}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creating admin user: {e}")
        db.rollback()
        return False
        
    finally:
        db.close()


if __name__ == "__main__":
    print("=" * 50)
    print("Create Admin User")
    print("=" * 50)
    
    if len(sys.argv) >= 3:
        email = sys.argv[1]
        password = sys.argv[2]
        full_name = sys.argv[3] if len(sys.argv) > 3 else "Administrator"
    else:
        email = input("Email: ")
        password = input("Password: ")
        full_name = input("Full Name (optional): ") or "Administrator"
    
    create_admin_user(email, password, full_name)
