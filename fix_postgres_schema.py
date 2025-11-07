#!/usr/bin/env python3
"""
Fix PostgreSQL schema to match SQLite schema
Adds missing columns to existing tables
"""

import os
import sys
import logging
from database import get_db, USE_POSTGRES

logging.basicConfig(level=logging.INFO)

def fix_users_table():
    """Add missing columns to users table"""
    conn = get_db()
    try:
        # Check and add missing columns
        columns_to_add = [
            ("first_name", "TEXT"),
            ("last_name", "TEXT"),
            ("mobile", "TEXT"),
            ("email", "TEXT"),
            ("profile_picture_path", "TEXT"),
            ("is_admin", "BOOLEAN DEFAULT FALSE"),
            ("enabled", "BOOLEAN DEFAULT TRUE"),
            ("created_at", "TEXT"),
            ("google_id", "TEXT UNIQUE")
        ]
        
        for col_name, col_type in columns_to_add:
            try:
                query = f"ALTER TABLE users ADD COLUMN {col_name} {col_type}"
                cursor = conn.execute(query)
                conn.commit()
                logging.info(f"✅ Added column: users.{col_name}")
            except Exception as e:
                conn.rollback()  # CRITICAL for PostgreSQL - must rollback on error
                if "already exists" in str(e) or "duplicate column" in str(e).lower():
                    logging.info(f"⏭️  Column already exists: users.{col_name}")
                else:
                    logging.warning(f"⚠️  Could not add users.{col_name}: {e}")
        
        conn.close()
        return True
    except Exception as e:
        logging.error(f"❌ Error fixing users table: {e}")
        return False

def fix_system_logs_table():
    """Add missing columns to system_logs table"""
    conn = get_db()
    try:
        columns_to_add = [
            ("module", "TEXT"),
            ("function", "TEXT"),
            ("line_number", "INTEGER"),
            ("exception", "TEXT")
        ]
        
        for col_name, col_type in columns_to_add:
            try:
                query = f"ALTER TABLE system_logs ADD COLUMN {col_name} {col_type}"
                cursor = conn.execute(query)
                conn.commit()
                logging.info(f"✅ Added column: system_logs.{col_name}")
            except Exception as e:
                conn.rollback()  # CRITICAL for PostgreSQL - must rollback on error
                if "already exists" in str(e) or "duplicate column" in str(e).lower():
                    logging.info(f"⏭️  Column already exists: system_logs.{col_name}")
                else:
                    logging.warning(f"⚠️  Could not add system_logs.{col_name}: {e}")
        
        conn.close()
        return True
    except Exception as e:
        logging.error(f"❌ Error fixing system_logs table: {e}")
        return False

def main():
    if not USE_POSTGRES:
        print("❌ This script is for PostgreSQL only")
        print("💡 Set DATABASE_URL environment variable")
        return False
    
    print("="*60)
    print("🔧 FIXING POSTGRESQL SCHEMA")
    print("="*60)
    print()
    
    success = True
    
    print("📊 Fixing users table...")
    if fix_users_table():
        print("✅ users table fixed\n")
    else:
        print("❌ users table failed\n")
        success = False
    
    print("📊 Fixing system_logs table...")
    if fix_system_logs_table():
        print("✅ system_logs table fixed\n")
    else:
        print("❌ system_logs table failed\n")
        success = False
    
    print("="*60)
    if success:
        print("✅ SCHEMA FIX COMPLETE!")
    else:
        print("⚠️  SCHEMA FIX COMPLETED WITH WARNINGS")
    print("="*60)
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
