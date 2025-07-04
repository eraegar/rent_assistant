"""
Migration script to add ClientAssistantAssignment table
Run this to add permanent client-assistant assignments to the database
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine
from database import SQLALCHEMY_DATABASE_URL
from models import Base, ClientAssistantAssignment

def migrate_add_assignments():
    """Add the client_assistant_assignments table"""
    engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
    
    # Create the table directly
    try:
        Base.metadata.create_all(engine, tables=[ClientAssistantAssignment.__table__])
        print("✅ ClientAssistantAssignment table created successfully")
    except Exception as e:
        print(f"❌ Error creating table: {e}")

if __name__ == "__main__":
    print("🔄 Running migration to add client-assistant assignments...")
    migrate_add_assignments()
    print("✅ Migration completed!") 