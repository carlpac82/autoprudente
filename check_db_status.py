#!/usr/bin/env python3
"""
Quick Database Status Check
Run this in Render Shell to verify PostgreSQL is working
"""

import os
import sys

print("=" * 60)
print("🔍 DATABASE STATUS CHECK")
print("=" * 60)

# Check DATABASE_URL
DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL:
    print("✅ DATABASE_URL is set")
    # Show partial URL (hide password)
    parts = DATABASE_URL.split('@')
    if len(parts) == 2:
        host_db = parts[1]
        print(f"📍 Host: {host_db}")
    else:
        print(f"📍 URL: {DATABASE_URL[:30]}...")
else:
    print("❌ DATABASE_URL is NOT set")
    print("💡 Using SQLite (local development mode)")
    sys.exit(1)

print("-" * 60)

# Check if database module loads
try:
    from database import USE_POSTGRES, get_db_connection
    print("✅ Database module loaded")
    
    if USE_POSTGRES:
        print("✅ PostgreSQL mode ENABLED")
    else:
        print("❌ PostgreSQL mode DISABLED (using SQLite)")
        sys.exit(1)
except ImportError as e:
    print(f"❌ Failed to import database module: {e}")
    sys.exit(1)

print("-" * 60)

# Test connection
try:
    print("🔌 Testing connection...")
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        # Get PostgreSQL version
        cursor.execute("SELECT version();")
        version = cursor.fetchone()[0]
        print(f"✅ Connected to PostgreSQL!")
        print(f"📊 Version: {version.split(',')[0]}")
        
        # Check if tables exist
        cursor.execute("""
            SELECT COUNT(*) 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
        """)
        table_count = cursor.fetchone()[0]
        print(f"📋 Tables found: {table_count}")
        
        if table_count == 0:
            print("⚠️  No tables found - run: python init_postgres.py")
        elif table_count < 22:
            print(f"⚠️  Only {table_count}/22 tables - run: python init_postgres.py")
        else:
            print(f"✅ All {table_count} tables exist!")
        
        conn.commit()
        
except Exception as e:
    print(f"❌ Connection failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("=" * 60)
print("🎉 PostgreSQL is working correctly!")
print("=" * 60)

# Show next steps
if table_count == 0:
    print("\n📝 NEXT STEP:")
    print("   Run: python init_postgres.py")
elif table_count < 22:
    print("\n📝 NEXT STEP:")
    print("   Run: python init_postgres.py")
else:
    print("\n✅ ALL DONE! Database is ready to use!")
    print("💡 You can now use the application normally.")
