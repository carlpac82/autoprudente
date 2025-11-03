"""
Initialize PostgreSQL Database
Creates all tables with PostgreSQL-compatible syntax
"""

import os
import sys
import logging
from database import get_db_connection, USE_POSTGRES

logging.basicConfig(level=logging.INFO)

def init_postgres_tables():
    """Create all tables in PostgreSQL"""
    
    if not USE_POSTGRES:
        print("❌ DATABASE_URL not set. This script is for PostgreSQL initialization only.")
        print("💡 For local development, the app will use SQLite automatically.")
        return
    
    print("🐘 Initializing PostgreSQL database...")
    
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        # 1. App Settings
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS app_settings (
                key VARCHAR(255) PRIMARY KEY,
                value TEXT
            )
        """)
        print("✅ Table: app_settings")
        
        # 2. Users
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username VARCHAR(255) UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                is_admin BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("✅ Table: users")
        
        # 3. Activity Log
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS activity_log (
                id SERIAL PRIMARY KEY,
                ts_utc TIMESTAMP NOT NULL,
                username VARCHAR(255),
                action VARCHAR(255),
                details TEXT,
                ip VARCHAR(45),
                user_agent TEXT
            )
        """)
        print("✅ Table: activity_log")
        
        # 4. Price Snapshots
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS price_snapshots (
                id SERIAL PRIMARY KEY,
                ts TIMESTAMP NOT NULL,
                location VARCHAR(255) NOT NULL,
                grupo VARCHAR(50) NOT NULL,
                days INTEGER NOT NULL,
                real_price DOUBLE PRECISION,
                net_price DOUBLE PRECISION,
                data_json TEXT
            )
        """)
        print("✅ Table: price_snapshots")
        
        # 5. Price Automation Settings
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS price_automation_settings (
                setting_key VARCHAR(255) PRIMARY KEY,
                setting_value TEXT NOT NULL,
                setting_type VARCHAR(50) DEFAULT 'string',
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("✅ Table: price_automation_settings")
        
        # 6. Automated Price Rules
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS automated_price_rules (
                id SERIAL PRIMARY KEY,
                location VARCHAR(255) NOT NULL,
                grupo VARCHAR(50) NOT NULL,
                month VARCHAR(20) NOT NULL,
                day INTEGER NOT NULL,
                rules_json TEXT NOT NULL,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("✅ Table: automated_price_rules")
        
        # 7. Pricing Strategies
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS pricing_strategies (
                id SERIAL PRIMARY KEY,
                location VARCHAR(255) NOT NULL,
                grupo VARCHAR(50) NOT NULL,
                month VARCHAR(20) NOT NULL,
                day INTEGER NOT NULL,
                year INTEGER NOT NULL,
                strategies_json TEXT NOT NULL,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("✅ Table: pricing_strategies")
        
        # 8. Automated Prices History
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS automated_prices_history (
                id SERIAL PRIMARY KEY,
                location VARCHAR(255) NOT NULL,
                grupo VARCHAR(50) NOT NULL,
                month VARCHAR(20) NOT NULL,
                year INTEGER NOT NULL,
                prices_json TEXT NOT NULL,
                saved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("✅ Table: automated_prices_history")
        
        # 9. System Logs
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS system_logs (
                id SERIAL PRIMARY KEY,
                level VARCHAR(20) NOT NULL,
                message TEXT NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                context TEXT
            )
        """)
        print("✅ Table: system_logs")
        
        # 10. Cache Data
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS cache_data (
                key VARCHAR(255) PRIMARY KEY,
                value TEXT NOT NULL,
                expires_at TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("✅ Table: cache_data")
        
        # 11. File Storage
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS file_storage (
                id SERIAL PRIMARY KEY,
                filename VARCHAR(255) NOT NULL,
                filepath VARCHAR(500) NOT NULL UNIQUE,
                file_data BYTEA,
                content_type VARCHAR(100),
                size_bytes INTEGER,
                uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("✅ Table: file_storage")
        
        # 12. Export History
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS export_history (
                id SERIAL PRIMARY KEY,
                filename VARCHAR(255) NOT NULL,
                broker VARCHAR(100) NOT NULL,
                location VARCHAR(255),
                month VARCHAR(20),
                year INTEGER,
                export_type VARCHAR(50),
                exported_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                file_data BYTEA
            )
        """)
        print("✅ Table: export_history")
        
        # 13. AI Learning Data
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ai_learning_data (
                id SERIAL PRIMARY KEY,
                grupo VARCHAR(50) NOT NULL,
                days INTEGER NOT NULL,
                real_price DOUBLE PRECISION NOT NULL,
                net_price DOUBLE PRECISION NOT NULL,
                margin_percent DOUBLE PRECISION,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("✅ Table: ai_learning_data")
        
        # 14. User Settings
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_settings (
                user_key VARCHAR(255) NOT NULL,
                setting_key VARCHAR(255) NOT NULL,
                setting_value TEXT NOT NULL,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (user_key, setting_key)
            )
        """)
        print("✅ Table: user_settings")
        
        # 15. Vans Pricing
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS vans_pricing (
                id SERIAL PRIMARY KEY,
                c3_1day DOUBLE PRECISION DEFAULT 112.00,
                c3_2days DOUBLE PRECISION DEFAULT 144.00,
                c3_3days DOUBLE PRECISION DEFAULT 168.00,
                c4_1day DOUBLE PRECISION DEFAULT 128.00,
                c4_2days DOUBLE PRECISION DEFAULT 160.00,
                c4_3days DOUBLE PRECISION DEFAULT 192.00,
                c5_1day DOUBLE PRECISION DEFAULT 144.00,
                c5_2days DOUBLE PRECISION DEFAULT 176.00,
                c5_3days DOUBLE PRECISION DEFAULT 216.00,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("✅ Table: vans_pricing")
        
        # 16. Custom Days
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS custom_days (
                id SERIAL PRIMARY KEY,
                days_array TEXT NOT NULL,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("✅ Table: custom_days")
        
        # 17. Price Validation Rules
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS price_validation_rules (
                id SERIAL PRIMARY KEY,
                rules_json TEXT NOT NULL,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                active BOOLEAN DEFAULT TRUE
            )
        """)
        print("✅ Table: price_validation_rules")
        
        # 18. Price History
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS price_history (
                id SERIAL PRIMARY KEY,
                history_type VARCHAR(50) NOT NULL,
                year INTEGER NOT NULL,
                month VARCHAR(20) NOT NULL,
                location VARCHAR(255) NOT NULL,
                prices_json TEXT NOT NULL,
                saved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("✅ Table: price_history")
        
        # 19. Car Images
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS car_images (
                model_key VARCHAR(255) PRIMARY KEY,
                photo_url TEXT,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("✅ Table: car_images")
        
        # 20. Vehicle Photos
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS vehicle_photos (
                vehicle_name VARCHAR(255) PRIMARY KEY,
                photo_data BYTEA,
                photo_url TEXT,
                content_type VARCHAR(100),
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("✅ Table: vehicle_photos")
        
        # 21. Vehicle Name Overrides
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS vehicle_name_overrides (
                original_name VARCHAR(255) PRIMARY KEY,
                edited_name VARCHAR(255) NOT NULL,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("✅ Table: vehicle_name_overrides")
        
        # 22. Vehicle Images
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS vehicle_images (
                vehicle_key VARCHAR(255) PRIMARY KEY,
                image_data BYTEA NOT NULL,
                content_type VARCHAR(100) DEFAULT 'image/jpeg',
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("✅ Table: vehicle_images")
        
        conn.commit()
        print("\n🎉 PostgreSQL database initialized successfully!")
        print("📊 Total tables created: 22")

if __name__ == "__main__":
    try:
        init_postgres_tables()
    except Exception as e:
        print(f"\n❌ Error initializing database: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
