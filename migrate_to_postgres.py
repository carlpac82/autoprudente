"""
Migrate data from SQLite to PostgreSQL
Run this script to transfer all existing data to the new PostgreSQL database
"""

import sqlite3
import os
import sys
import logging
from database import get_db_connection, USE_POSTGRES

logging.basicConfig(level=logging.INFO)

def migrate_table(sqlite_conn, pg_conn, table_name, columns):
    """Migrate a single table from SQLite to PostgreSQL"""
    try:
        # Read from SQLite
        sqlite_cursor = sqlite_conn.cursor()
        sqlite_cursor.execute(f"SELECT * FROM {table_name}")
        rows = sqlite_cursor.fetchall()
        
        if not rows:
            print(f"  ⚠️  {table_name}: No data to migrate")
            return 0
        
        # Get column names
        col_names = [description[0] for description in sqlite_cursor.description]
        
        # Prepare INSERT statement for PostgreSQL
        placeholders = ', '.join(['%s'] * len(col_names))
        columns_str = ', '.join(col_names)
        insert_query = f"INSERT INTO {table_name} ({columns_str}) VALUES ({placeholders}) ON CONFLICT DO NOTHING"
        
        # Insert into PostgreSQL
        pg_cursor = pg_conn.cursor()
        count = 0
        for row in rows:
            try:
                pg_cursor.execute(insert_query, row)
                count += 1
            except Exception as e:
                logging.warning(f"Error inserting row into {table_name}: {e}")
                continue
        
        pg_conn.commit()
        print(f"  ✅ {table_name}: Migrated {count} rows")
        return count
        
    except sqlite3.OperationalError as e:
        if "no such table" in str(e):
            print(f"  ⚠️  {table_name}: Table doesn't exist in SQLite")
            return 0
        raise
    except Exception as e:
        print(f"  ❌ {table_name}: Error - {e}")
        return 0

def migrate_all_data():
    """Migrate all data from SQLite to PostgreSQL"""
    
    if not USE_POSTGRES:
        print("❌ DATABASE_URL not set. Cannot migrate to PostgreSQL.")
        print("💡 Set DATABASE_URL environment variable with your PostgreSQL connection string.")
        return
    
    print("🔄 Starting migration from SQLite to PostgreSQL...")
    print("=" * 60)
    
    # Connect to SQLite
    try:
        sqlite_conn = sqlite3.connect("data.db")
        print("✅ Connected to SQLite (data.db)")
    except Exception as e:
        print(f"❌ Error connecting to SQLite: {e}")
        return
    
    # Connect to PostgreSQL
    try:
        with get_db_connection() as pg_conn:
            print("✅ Connected to PostgreSQL")
            print("=" * 60)
            
            # Tables to migrate (in order to respect foreign keys)
            tables = [
                "app_settings",
                "users",
                "activity_log",
                "price_snapshots",
                "price_automation_settings",
                "automated_price_rules",
                "pricing_strategies",
                "automated_prices_history",
                "system_logs",
                "cache_data",
                "file_storage",
                "export_history",
                "ai_learning_data",
                "user_settings",
                "vans_pricing",
                "custom_days",
                "price_validation_rules",
                "price_history",
                "car_images",
                "vehicle_photos",
                "vehicle_name_overrides",
                "vehicle_images"
            ]
            
            total_rows = 0
            migrated_tables = 0
            
            for table in tables:
                print(f"\n📊 Migrating: {table}")
                count = migrate_table(sqlite_conn, pg_conn, table, None)
                if count > 0:
                    total_rows += count
                    migrated_tables += 1
            
            print("\n" + "=" * 60)
            print(f"🎉 Migration completed!")
            print(f"📊 Tables migrated: {migrated_tables}/{len(tables)}")
            print(f"📝 Total rows migrated: {total_rows}")
            print("=" * 60)
            
    except Exception as e:
        print(f"\n❌ Migration error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        sqlite_conn.close()

if __name__ == "__main__":
    migrate_all_data()
