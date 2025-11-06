#!/usr/bin/env python3
"""
Create recent_searches table in PostgreSQL (Render)
Run in Render Shell: python create_recent_searches_table.py
"""

import os
import psycopg2

def create_recent_searches_table():
    """Create recent_searches table in PostgreSQL"""
    
    database_url = os.environ.get('DATABASE_URL')
    
    if not database_url:
        print("❌ DATABASE_URL not found!")
        print("💡 This script must be run in Render Shell")
        return False
    
    try:
        print("🔍 Connecting to PostgreSQL...")
        conn = psycopg2.connect(database_url)
        cursor = conn.cursor()
        
        print("📋 Creating recent_searches table...")
        
        # Create table (PostgreSQL syntax)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS recent_searches (
                id SERIAL PRIMARY KEY,
                location TEXT NOT NULL,
                start_date TEXT NOT NULL,
                days INTEGER NOT NULL,
                results_data TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                "user" TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create index for faster queries
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_recent_searches_user 
            ON recent_searches("user", created_at DESC)
        """)
        
        conn.commit()
        
        print("✅ Table recent_searches created successfully!")
        
        # Verify
        cursor.execute("""
            SELECT COUNT(*) FROM recent_searches
        """)
        count = cursor.fetchone()[0]
        print(f"📊 Current records: {count}")
        
        cursor.close()
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"❌ Error creating table: {str(e)}")
        import traceback
        print(traceback.format_exc())
        return False

if __name__ == '__main__':
    print("="*60)
    print("🔧 CREATING RECENT_SEARCHES TABLE")
    print("="*60)
    print()
    
    success = create_recent_searches_table()
    
    print()
    print("="*60)
    if success:
        print("✅ SUCCESS!")
        print()
        print("💡 Now the homepage preview should work!")
    else:
        print("❌ FAILED!")
        print()
        print("💡 Make sure you run this in Render Shell:")
        print("   python create_recent_searches_table.py")
    print("="*60)
