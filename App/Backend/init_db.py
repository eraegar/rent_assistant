#!/usr/bin/env python3
"""
Database initialization script
Creates all tables and sets up the database schema
"""

from sqlalchemy import create_engine
from models import Base, User, Task
from database import engine

def init_database():
    """Initialize database by creating all tables"""
    print("🚀 Initializing database...")
    
    try:
        # Create all tables
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created successfully!")
        
        # List created tables
        from sqlalchemy import inspect
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        print(f"📊 Created tables: {tables}")
        
    except Exception as e:
        print(f"❌ Error creating database: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = init_database()
    if success:
        print("🎉 Database is ready to use!")
    else:
        print("💥 Database initialization failed!") 