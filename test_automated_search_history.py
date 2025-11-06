#!/usr/bin/env python3
"""
Test script to verify automated_search_history table and functionality
"""

import sqlite3
import json
from datetime import datetime

# Connect to local database
conn = sqlite3.connect('data.db')
cursor = conn.cursor()

print("=" * 60)
print("AUTOMATED SEARCH HISTORY - VERIFICATION")
print("=" * 60)

# 1. Check if table exists
cursor.execute("""
    SELECT name FROM sqlite_master 
    WHERE type='table' AND name='automated_search_history'
""")
table_exists = cursor.fetchone()

if table_exists:
    print("\n✅ Table 'automated_search_history' EXISTS")
    
    # Get table schema
    cursor.execute("PRAGMA table_info(automated_search_history)")
    columns = cursor.fetchall()
    print("\nTable Schema:")
    for col in columns:
        print(f"  - {col[1]} ({col[2]})")
    
    # Check data count
    cursor.execute("SELECT COUNT(*) FROM automated_search_history")
    count = cursor.fetchone()[0]
    print(f"\n📊 Total records: {count}")
    
    if count > 0:
        # Show recent records
        cursor.execute("""
            SELECT id, location, search_type, search_date, month_key, 
                   price_count, user_email
            FROM automated_search_history
            ORDER BY search_date DESC
            LIMIT 5
        """)
        
        print("\n📋 Recent Records:")
        for row in cursor.fetchall():
            print(f"\n  ID: {row[0]}")
            print(f"  Location: {row[1]}")
            print(f"  Type: {row[2]}")
            print(f"  Date: {row[3]}")
            print(f"  Month: {row[4]}")
            print(f"  Prices: {row[5]}")
            print(f"  User: {row[6]}")
    else:
        print("\n⚠️  No records found - table is empty")
        print("\nThis is normal if:")
        print("  1. No automated searches have been performed yet")
        print("  2. Searches were done before the fix was deployed")
        
else:
    print("\n❌ Table 'automated_search_history' DOES NOT EXIST")
    print("\nThe table should be created automatically on app startup.")
    print("Check main.py around line 2415 for table creation code.")

print("\n" + "=" * 60)
print("TESTING INSERT (if table exists)")
print("=" * 60)

if table_exists:
    try:
        # Test insert
        now = datetime.now()
        month_key = f"{now.year}-{str(now.month).zfill(2)}"
        
        test_prices = {
            "B1": {"31": 25.50, "60": 23.00},
            "D": {"31": 35.00, "60": 32.50}
        }
        test_dias = [31, 60, 90]
        
        cursor.execute("""
            INSERT INTO automated_search_history 
            (location, search_type, month_key, prices_data, dias, price_count, user_email)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            'Test Location',
            'automated',
            month_key,
            json.dumps(test_prices),
            json.dumps(test_dias),
            4,
            'test@example.com'
        ))
        
        test_id = cursor.lastrowid
        conn.commit()
        
        print(f"\n✅ Test insert successful! ID: {test_id}")
        
        # Clean up test data
        cursor.execute("DELETE FROM automated_search_history WHERE id = ?", (test_id,))
        conn.commit()
        print("✅ Test data cleaned up")
        
    except Exception as e:
        print(f"\n❌ Test insert failed: {str(e)}")
        conn.rollback()

conn.close()

print("\n" + "=" * 60)
print("RECOMMENDATION")
print("=" * 60)
print("""
To test the full flow:
1. Wait for Render deploy to complete (~5-10 minutes)
2. Go to https://your-app.onrender.com/price-automation
3. Generate automated prices
4. Check browser console for these logs:
   - "Sending to PostgreSQL:"
   - "Automated price history saved to PostgreSQL:"
   - "Saved X automated prices to history"
5. Check History tab for the saved search
""")
