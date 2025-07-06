#!/usr/bin/env python3
"""
Migration script to add password tracking fields to assistant_profiles table
"""
import sys
import os

# Добавляем путь к app папке
current_dir = os.path.dirname(os.path.abspath(__file__))
app_dir = os.path.dirname(current_dir)
sys.path.append(app_dir)

# Меняем рабочую директорию на app
os.chdir(app_dir)

from database import SessionLocal, engine
from sqlalchemy import text
from datetime import datetime

def migrate_add_password_fields():
    """Add password tracking fields to assistant_profiles"""
    
    db = SessionLocal()
    
    try:
        print("🔄 Adding password tracking fields to assistant_profiles table...")
        
        # Check if columns already exist
        result = db.execute(text("PRAGMA table_info(assistant_profiles)"))
        columns = [row[1] for row in result.fetchall()]
        
        print(f"📋 Current columns: {columns}")
        
        # Add last_known_password column if it doesn't exist
        if 'last_known_password' not in columns:
            print("➕ Adding last_known_password column...")
            db.execute(text("ALTER TABLE assistant_profiles ADD COLUMN last_known_password TEXT"))
            print("✅ Added last_known_password column")
        else:
            print("✅ last_known_password column already exists")
        
        # Add last_password_reset_at column if it doesn't exist  
        if 'last_password_reset_at' not in columns:
            print("➕ Adding last_password_reset_at column...")
            db.execute(text("ALTER TABLE assistant_profiles ADD COLUMN last_password_reset_at DATETIME"))
            print("✅ Added last_password_reset_at column")
        else:
            print("✅ last_password_reset_at column already exists")
        
        # For existing assistants, set known passwords based on test data
        print("\n🔧 Setting known passwords for existing assistants...")
        
        # Set password for Геннадий (we know it's qwqwqw)
        db.execute(text("""
            UPDATE assistant_profiles 
            SET last_known_password = 'qwqwqw', 
                last_password_reset_at = :reset_time
            WHERE user_id = (
                SELECT id FROM users 
                WHERE name LIKE '%Геннадий%' AND role = 'assistant'
            )
        """), {"reset_time": datetime.utcnow()})
        
        # Set default password for other test assistants
        db.execute(text("""
            UPDATE assistant_profiles 
            SET last_known_password = 'assistant123', 
                last_password_reset_at = :reset_time
            WHERE user_id IN (
                SELECT id FROM users 
                WHERE role = 'assistant' AND name NOT LIKE '%Геннадий%'
            ) AND last_known_password IS NULL
        """), {"reset_time": datetime.utcnow()})
        
        db.commit()
        print("✅ Migration completed successfully!")
        
        # Verify the changes
        print("\n📊 Verification:")
        result = db.execute(text("""
            SELECT u.name, ap.last_known_password, ap.last_password_reset_at 
            FROM assistant_profiles ap
            JOIN users u ON ap.user_id = u.id 
            WHERE u.role = 'assistant'
        """))
        
        for row in result.fetchall():
            print(f"  {row[0]}: password='{row[1]}', reset_at={row[2]}")
        
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    migrate_add_password_fields() 