#!/usr/bin/env python3
"""
Verificar se as regras estão guardadas na database do Render
"""
import os
import psycopg2
from urllib.parse import urlparse

# Get database URL from environment
database_url = os.getenv('DATABASE_URL')

if not database_url:
    print("❌ DATABASE_URL não encontrada!")
    print("Execute: export DATABASE_URL='postgres://...'")
    exit(1)

# Parse URL
result = urlparse(database_url)
username = result.username
password = result.password
database = result.path[1:]
hostname = result.hostname
port = result.port

print(f"🔗 Connecting to: {hostname}:{port}/{database}")

try:
    conn = psycopg2.connect(
        database=database,
        user=username,
        password=password,
        host=hostname,
        port=port
    )
    
    cursor = conn.cursor()
    
    # Check if table exists
    cursor.execute("""
        SELECT EXISTS (
            SELECT FROM information_schema.tables 
            WHERE table_name = 'automated_price_rules'
        )
    """)
    
    if not cursor.fetchone()[0]:
        print("❌ Tabela 'automated_price_rules' NÃO EXISTE!")
        exit(1)
    
    print("✅ Tabela 'automated_price_rules' existe")
    
    # Count rules
    cursor.execute("SELECT COUNT(*) FROM automated_price_rules")
    count = cursor.fetchone()[0]
    
    print(f"\n📊 TOTAL DE REGRAS NA DATABASE: {count}")
    
    if count == 0:
        print("\n❌ NENHUMA REGRA ENCONTRADA!")
        print("Isto confirma que as regras NUNCA foram guardadas na database.")
    else:
        print(f"\n✅ {count} regras encontradas!")
        
        # Show sample rules
        cursor.execute("""
            SELECT location, grupo, month, day, config 
            FROM automated_price_rules 
            LIMIT 5
        """)
        
        print("\n📋 EXEMPLOS DE REGRAS:")
        for row in cursor.fetchall():
            location, grupo, month, day, config = row
            print(f"  - {location}/{grupo}/M{month}/D{day}: {config[:100]}...")
        
        # Show locations and groups
        cursor.execute("""
            SELECT DISTINCT location, COUNT(DISTINCT grupo) as num_grupos
            FROM automated_price_rules
            GROUP BY location
        """)
        
        print("\n📍 LOCALIZAÇÕES:")
        for row in cursor.fetchall():
            location, num_grupos = row
            print(f"  - {location}: {num_grupos} grupos")
    
    conn.close()
    
except Exception as e:
    print(f"❌ ERRO: {e}")
    exit(1)
