import sys
import os
from app.db.session import engine
from app.database import Base
# Import all models to register them in SQLAlchemy metadata
from app.models.user import User
from app.models.role import Role
from app.models.permission import Permission
from app.models.user_role import UserRole
from app.models.role_permission import RolePermission

# Trying to import the seed function
try:
    from app.db.feed_rbac import seed_rbac
except ImportError:
    from app.db.seed_rbac import seed_rbac

def setup():
    """
    Main database setup script: creates tables and populates initial data.
    """
    print("--- Starting Database Setup ---")
    
    # Create all tables defined in Base.metadata
    print("Step 1: Creating tables...")
    Base.metadata.create_all(bind=engine)
    print("Result: Tables created successfully.")
    
    # Run the seed function to add Admin and Roles
    print("Step 2: Seeding initial data...")
    seed_rbac()
    print("Result: Seeding completed.")
    
    print("--- Setup Finished! You can run the server now ---")

if __name__ == "__main__":
    setup()