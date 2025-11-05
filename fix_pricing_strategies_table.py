#!/usr/bin/env python3
"""
Script para corrigir a tabela pricing_strategies no PostgreSQL
Adiciona a coluna 'priority' se não existir
Executar no Render Shell: python fix_pricing_strategies_table.py
"""

import os
import psycopg2
from urllib.parse import urlparse

def fix_pricing_strategies():
    """Adicionar coluna priority à tabela pricing_strategies"""
    
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
    print("🔧 FIXING pricing_strategies TABLE")
    print("=" * 80)
    
    # Check if column exists
    print("\n1️⃣ Checking if 'priority' column exists...")
    cursor.execute("""
        SELECT column_name 
        FROM information_schema.columns 
        WHERE table_name = 'pricing_strategies' 
        AND column_name = 'priority'
    """)
    
    if cursor.fetchone():
        print("   ✅ Column 'priority' already exists - nothing to do!")
    else:
        print("   ⚠️  Column 'priority' does NOT exist - adding it...")
        
        # Add the column
        cursor.execute("""
            ALTER TABLE pricing_strategies 
            ADD COLUMN priority INTEGER NOT NULL DEFAULT 1
        """)
        
        print("   ✅ Column 'priority' added successfully!")
    
    # Create index if not exists
    print("\n2️⃣ Creating index on pricing_strategies...")
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_strategies 
        ON pricing_strategies(location, grupo, month, day, priority)
    """)
    print("   ✅ Index created successfully!")
    
    # Commit changes
    conn.commit()
    cursor.close()
    conn.close()
    
    print("\n" + "=" * 80)
    print("✅ FIX COMPLETED SUCCESSFULLY!")
    print("=" * 80)
    print("\n📋 NEXT STEPS:")
    print("   1. Restart the Render service")
    print("   2. Check logs - should start without errors")
    print("\n🎉 ALL DONE!")

if __name__ == "__main__":
    fix_pricing_strategies()
