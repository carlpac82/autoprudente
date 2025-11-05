#!/usr/bin/env python3
"""
Script SEGURO para criar TODAS as tabelas no PostgreSQL do Render
NÃO crashará se colunas não existirem nos índices
Executar no Render Shell: python migrate_all_tables_postgres_safe.py
"""

import os
import psycopg2
from urllib.parse import urlparse

def safe_create_index(cursor, conn, index_sql, index_name):
    """Safely create index - won't crash if columns don't exist"""
    try:
        cursor.execute(index_sql)
        print(f"   ✅ {index_name} created")
    except Exception as idx_err:
        print(f"   ⚠️  {index_name} skipped: {idx_err}")
        conn.rollback()

def migrate_database():
    """Criar todas as tabelas necessárias no PostgreSQL"""
    
    # Get DATABASE_URL from environment
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        print("❌ DATABASE_URL not found!")
        return
    
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
    
    print("=" * 80)
    print("🔧 CREATING ALL TABLES IN POSTGRESQL (SAFE MODE)")
    print("=" * 80)
    
    # 1. price_snapshots
    print("\n1️⃣ Creating price_snapshots table...")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS price_snapshots (
          id SERIAL PRIMARY KEY,
          ts TEXT NOT NULL,
          location TEXT NOT NULL,
          pickup_date TEXT NOT NULL,
          pickup_time TEXT NOT NULL,
          days INTEGER NOT NULL,
          supplier TEXT,
          car TEXT,
          price_text TEXT,
          price_num DOUBLE PRECISION,
          currency TEXT,
          link TEXT
        )
    """)
    print("   ✅ price_snapshots created")
    safe_create_index(cursor, conn, "CREATE INDEX IF NOT EXISTS idx_snapshots_q ON price_snapshots(location, days, ts)", "idx_snapshots_q")
    
    # 2. automated_price_rules
    print("\n2️⃣ Creating automated_price_rules table...")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS automated_price_rules (
          id SERIAL PRIMARY KEY,
          location TEXT NOT NULL,
          grupo TEXT NOT NULL,
          month INTEGER,
          day INTEGER,
          config TEXT NOT NULL,
          created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
          updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
          UNIQUE(location, grupo, month, day)
        )
    """)
    print("   ✅ automated_price_rules created")
    
    # 3. pricing_strategies
    print("\n3️⃣ Creating pricing_strategies table...")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pricing_strategies (
          id SERIAL PRIMARY KEY,
          location TEXT NOT NULL,
          grupo TEXT NOT NULL,
          month INTEGER,
          day INTEGER,
          priority INTEGER NOT NULL DEFAULT 1,
          strategy_type TEXT NOT NULL,
          config TEXT NOT NULL,
          created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
          updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    print("   ✅ pricing_strategies created")
    safe_create_index(cursor, conn, "CREATE INDEX IF NOT EXISTS idx_strategies ON pricing_strategies(location, grupo, month, day, priority)", "idx_strategies")
    
    # 4. automated_prices_history
    print("\n4️⃣ Creating automated_prices_history table...")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS automated_prices_history (
          id SERIAL PRIMARY KEY,
          location TEXT NOT NULL,
          grupo TEXT NOT NULL,
          dias INTEGER NOT NULL,
          pickup_date TEXT NOT NULL,
          auto_price DOUBLE PRECISION NOT NULL,
          real_price DOUBLE PRECISION NOT NULL,
          strategy_used TEXT,
          strategy_details TEXT,
          min_price_applied DOUBLE PRECISION,
          created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
          created_by TEXT
        )
    """)
    print("   ✅ automated_prices_history created")
    safe_create_index(cursor, conn, "CREATE INDEX IF NOT EXISTS idx_auto_prices_history ON automated_prices_history(location, grupo, pickup_date, created_at)", "idx_auto_prices_history")
    
    # 5. system_logs
    print("\n5️⃣ Creating system_logs table...")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS system_logs (
          id SERIAL PRIMARY KEY,
          level TEXT NOT NULL,
          message TEXT NOT NULL,
          module TEXT,
          function TEXT,
          line_number INTEGER,
          exception TEXT,
          created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    print("   ✅ system_logs created")
    safe_create_index(cursor, conn, "CREATE INDEX IF NOT EXISTS idx_system_logs ON system_logs(level, created_at)", "idx_system_logs")
    
    # 6. cache_data
    print("\n6️⃣ Creating cache_data table...")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cache_data (
          key TEXT PRIMARY KEY,
          value TEXT NOT NULL,
          expires_at TEXT,
          created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
          updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    print("   ✅ cache_data created")
    
    # 7. file_storage
    print("\n7️⃣ Creating file_storage table...")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS file_storage (
          id SERIAL PRIMARY KEY,
          filename TEXT NOT NULL,
          filepath TEXT NOT NULL UNIQUE,
          file_data BYTEA NOT NULL,
          content_type TEXT,
          file_size INTEGER,
          uploaded_by TEXT,
          created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    print("   ✅ file_storage created")
    safe_create_index(cursor, conn, "CREATE INDEX IF NOT EXISTS idx_file_storage ON file_storage(filepath, uploaded_by)", "idx_file_storage")
    
    # 8. export_history
    print("\n8️⃣ Creating export_history table...")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS export_history (
          id SERIAL PRIMARY KEY,
          filename TEXT NOT NULL,
          broker TEXT NOT NULL,
          location TEXT NOT NULL,
          period_start INTEGER,
          period_end INTEGER,
          month INTEGER NOT NULL,
          year INTEGER NOT NULL,
          month_name TEXT NOT NULL,
          file_content TEXT NOT NULL,
          file_size INTEGER,
          exported_by TEXT,
          export_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
          last_downloaded TEXT
        )
    """)
    print("   ✅ export_history created")
    safe_create_index(cursor, conn, "CREATE INDEX IF NOT EXISTS idx_export_history ON export_history(broker, location, year, month, export_date)", "idx_export_history")
    
    # 9. ai_learning_data
    print("\n9️⃣ Creating ai_learning_data table...")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ai_learning_data (
          id SERIAL PRIMARY KEY,
          grupo TEXT NOT NULL,
          days INTEGER NOT NULL,
          location TEXT NOT NULL,
          original_price DOUBLE PRECISION,
          new_price DOUBLE PRECISION NOT NULL,
          timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
          "user" TEXT DEFAULT 'admin'
        )
    """)
    print("   ✅ ai_learning_data created")
    safe_create_index(cursor, conn, "CREATE INDEX IF NOT EXISTS idx_ai_learning ON ai_learning_data(grupo, days, location, timestamp DESC)", "idx_ai_learning")
    
    # 10. user_settings
    print("\n🔟 Creating user_settings table...")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_settings (
          user_key TEXT NOT NULL,
          setting_key TEXT NOT NULL,
          setting_value TEXT NOT NULL,
          updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
          PRIMARY KEY (user_key, setting_key)
        )
    """)
    print("   ✅ user_settings created")
    safe_create_index(cursor, conn, "CREATE INDEX IF NOT EXISTS idx_user_settings ON user_settings(user_key, updated_at DESC)", "idx_user_settings")
    
    # 11. price_automation_settings
    print("\n1️⃣1️⃣ Creating price_automation_settings table...")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS price_automation_settings (
          setting_key TEXT PRIMARY KEY,
          setting_value TEXT NOT NULL,
          setting_type TEXT DEFAULT 'string',
          updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    print("   ✅ price_automation_settings created")
    
    # 12. price_history
    print("\n1️⃣2️⃣ Creating price_history table...")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS price_history (
          id SERIAL PRIMARY KEY,
          history_type TEXT NOT NULL,
          year INTEGER NOT NULL,
          month INTEGER NOT NULL,
          location TEXT NOT NULL,
          prices_data TEXT NOT NULL,
          saved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
          saved_by TEXT DEFAULT 'admin'
        )
    """)
    print("   ✅ price_history created")
    safe_create_index(cursor, conn, "CREATE INDEX IF NOT EXISTS idx_price_history ON price_history(history_type, year, month, location, saved_at DESC)", "idx_price_history")
    
    # 13. search_history
    print("\n1️⃣3️⃣ Creating search_history table...")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS search_history (
          id SERIAL PRIMARY KEY,
          location TEXT NOT NULL,
          start_date TEXT NOT NULL,
          end_date TEXT NOT NULL,
          days INTEGER NOT NULL,
          results_count INTEGER,
          min_price DOUBLE PRECISION,
          max_price DOUBLE PRECISION,
          avg_price DOUBLE PRECISION,
          search_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
          "user" TEXT DEFAULT 'admin',
          search_params TEXT
        )
    """)
    print("   ✅ search_history created")
    safe_create_index(cursor, conn, "CREATE INDEX IF NOT EXISTS idx_search_history ON search_history(location, start_date, search_timestamp DESC)", "idx_search_history")
    
    # 14. notification_rules
    print("\n1️⃣4️⃣ Creating notification_rules table...")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notification_rules (
          id SERIAL PRIMARY KEY,
          rule_name TEXT NOT NULL,
          rule_type TEXT NOT NULL,
          condition_json TEXT NOT NULL,
          action_json TEXT NOT NULL,
          enabled INTEGER DEFAULT 1,
          priority INTEGER DEFAULT 1,
          created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
          updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
          created_by TEXT DEFAULT 'admin'
        )
    """)
    print("   ✅ notification_rules created")
    safe_create_index(cursor, conn, "CREATE INDEX IF NOT EXISTS idx_notification_rules ON notification_rules(enabled, priority, rule_type)", "idx_notification_rules")
    
    # 15. notification_history
    print("\n1️⃣5️⃣ Creating notification_history table...")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notification_history (
          id SERIAL PRIMARY KEY,
          rule_id INTEGER,
          notification_type TEXT NOT NULL,
          recipient TEXT NOT NULL,
          subject TEXT,
          message TEXT NOT NULL,
          sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
          status TEXT DEFAULT 'sent',
          error_message TEXT
        )
    """)
    print("   ✅ notification_history created")
    safe_create_index(cursor, conn, "CREATE INDEX IF NOT EXISTS idx_notification_history ON notification_history(sent_at DESC, status)", "idx_notification_history")
    
    conn.commit()
    cursor.close()
    conn.close()
    
    print("\n" + "=" * 80)
    print("✅ MIGRATION COMPLETED SUCCESSFULLY!")
    print("=" * 80)
    print("\n📊 SUMMARY:")
    print("   ✅ 15 tables created in PostgreSQL")
    print("   ✅ All indexes created (or skipped if columns missing)")
    print("   ✅ Database ready for production")
    print("\n📋 NEXT STEPS:")
    print("   1. Restart the Render service (or it will restart automatically)")
    print("   2. Check logs for: '✅ All tables created/verified'")
    print("   3. Test AI learning, price history, and automated searches")
    print("\n🎉 ALL DONE!")

if __name__ == "__main__":
    migrate_database()
