#!/usr/bin/env python3
"""
Script para criar tabelas faltantes no PostgreSQL do Render
Executar no Render Shell: python migrate_render_db.py
"""

import os
import psycopg2
from urllib.parse import urlparse

def migrate_database():
    """Criar tabelas oauth_tokens e notification_rules no PostgreSQL"""
    
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
    
    print("🔧 Creating oauth_tokens table...")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS oauth_tokens (
          id SERIAL PRIMARY KEY,
          provider TEXT NOT NULL,
          user_email TEXT NOT NULL,
          access_token TEXT NOT NULL,
          refresh_token TEXT,
          expires_at BIGINT,
          google_id TEXT,
          user_name TEXT,
          user_picture TEXT,
          created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
          updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
          UNIQUE(provider, user_email)
        )
    """)
    print("✅ oauth_tokens table created!")
    
    print("🔧 Creating notification_rules table...")
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
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_notification_rules ON notification_rules(enabled, priority, rule_type)")
    print("✅ notification_rules table created!")
    
    print("🔧 Creating notification_history table...")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notification_history (
          id SERIAL PRIMARY KEY,
          rule_id INTEGER,
          notification_type TEXT NOT NULL,
          recipient TEXT NOT NULL,
          subject TEXT,
          message TEXT,
          status TEXT NOT NULL,
          error_message TEXT,
          sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_notification_history ON notification_history(sent_at DESC, status)")
    print("✅ notification_history table created!")
    
    conn.commit()
    cursor.close()
    conn.close()
    
    print("\n✅ Migration completed successfully!")
    print("\n📋 Next steps:")
    print("1. Restart the Render service")
    print("2. Connect Gmail OAuth")
    print("3. Test emails")

if __name__ == "__main__":
    migrate_database()
