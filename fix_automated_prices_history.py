#!/usr/bin/env python3
"""
Migration Script: Fix automated_prices_history table
Adds missing 'auto_price' and 'source' columns if they don't exist
"""

import os
import sys
import psycopg2
from urllib.parse import urlparse

def fix_automated_prices_history_table():
    """Add missing columns to automated_prices_history table"""
    
    # Get DATABASE_URL from environment
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        print("❌ DATABASE_URL not found! Set it in your environment or .env file")
        print("   Example: export DATABASE_URL='postgresql://user:password@host:port/database'")
        return False
    
    print("\n" + "="*80)
    print("🔧 FIXING automated_prices_history TABLE")
    print("="*80)
    
    try:
        # Parse URL
        result = urlparse(database_url)
        
        # Connect to PostgreSQL
        conn = psycopg2.connect(
            database=result.path[1:],
            user=result.username,
            password=result.password,
            host=result.hostname,
            port=result.port
        )
        
        cursor = conn.cursor()
        
        print("\n📊 Checking current table schema...")
        cursor.execute("""
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_name='automated_prices_history'
            ORDER BY ordinal_position
        """)
        
        existing_columns = {row[0]: row[1] for row in cursor.fetchall()}
        print(f"   ✅ Found table with {len(existing_columns)} columns")
        print(f"   Current columns: {list(existing_columns.keys())}")
        
        # Track changes
        changes_made = []
        
        # Check and add 'auto_price' column if missing
        if 'auto_price' not in existing_columns:
            print("\n❌ Missing column: auto_price")
            print("   Adding column...")
            cursor.execute("""
                ALTER TABLE automated_prices_history 
                ADD COLUMN auto_price DOUBLE PRECISION
            """)
            conn.commit()
            print("   ✅ Added 'auto_price' column (DOUBLE PRECISION)")
            changes_made.append("auto_price")
        else:
            print(f"\n✅ Column 'auto_price' already exists ({existing_columns['auto_price']})")
        
        # Check and add 'source' column if missing
        if 'source' not in existing_columns:
            print("\n❌ Missing column: source")
            print("   Adding column...")
            cursor.execute("""
                ALTER TABLE automated_prices_history 
                ADD COLUMN source TEXT DEFAULT 'manual'
            """)
            conn.commit()
            print("   ✅ Added 'source' column (TEXT, default='manual')")
            changes_made.append("source")
        else:
            print(f"\n✅ Column 'source' already exists ({existing_columns['source']})")
        
        # Verify final schema
        print("\n📊 Verifying final schema...")
        cursor.execute("""
            SELECT column_name, data_type, is_nullable, column_default
            FROM information_schema.columns 
            WHERE table_name='automated_prices_history'
            ORDER BY ordinal_position
        """)
        
        print("\n📋 FINAL TABLE SCHEMA:")
        print("   " + "-"*70)
        print(f"   {'Column':<25} {'Type':<20} {'Nullable':<10} {'Default':<15}")
        print("   " + "-"*70)
        for row in cursor.fetchall():
            col_name, data_type, nullable, default = row
            nullable_str = "YES" if nullable == "YES" else "NO"
            default_str = str(default)[:15] if default else "-"
            print(f"   {col_name:<25} {data_type:<20} {nullable_str:<10} {default_str:<15}")
        print("   " + "-"*70)
        
        cursor.close()
        conn.close()
        
        # Summary
        print("\n" + "="*80)
        if changes_made:
            print("✅ MIGRATION COMPLETED SUCCESSFULLY!")
            print(f"   Columns added: {', '.join(changes_made)}")
        else:
            print("✅ TABLE ALREADY UP TO DATE!")
            print("   No changes needed")
        print("="*80)
        
        print("\n📋 NEXT STEPS:")
        print("   1. Restart your application")
        print("   2. Test the automated price saving functionality")
        print("   3. Check logs for successful INSERT operations")
        print("\n🎉 ALL DONE!\n")
        
        return True
        
    except psycopg2.Error as e:
        print(f"\n❌ PostgreSQL Error: {e}")
        print(f"   Error Code: {e.pgcode}")
        print(f"   Details: {e.pgerror}")
        return False
    except Exception as e:
        print(f"\n❌ Unexpected Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = fix_automated_prices_history_table()
    sys.exit(0 if success else 1)
