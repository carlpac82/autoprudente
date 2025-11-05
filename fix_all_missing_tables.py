#!/usr/bin/env python3
"""
Script para criar TODAS as tabelas em falta no PostgreSQL
Execute no Render Shell se houver erros de "no such table"
"""

import os
import psycopg2
from psycopg2 import sql

def create_all_tables():
    """Criar todas as tabelas necessárias"""
    
    # Get database URL from environment
    database_url = os.environ.get('DATABASE_URL')
    
    if not database_url:
        print("❌ DATABASE_URL não encontrado!")
        print("   Este script deve ser executado no Render Shell")
        return False
    
    try:
        print("=" * 80)
        print("🔧 CRIANDO TODAS AS TABELAS NECESSÁRIAS")
        print("=" * 80)
        print()
        
        # Connect to PostgreSQL
        conn = psycopg2.connect(database_url)
        cursor = conn.cursor()
        
        tables_created = []
        
        # 1. price_snapshots
        print("1️⃣  Criando tabela price_snapshots...")
        try:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS price_snapshots (
                    id SERIAL PRIMARY KEY,
                    location TEXT NOT NULL,
                    pickup_date TEXT NOT NULL,
                    days INTEGER NOT NULL,
                    car TEXT NOT NULL,
                    "group" TEXT,
                    supplier TEXT,
                    price REAL,
                    snapshot_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    search_id TEXT
                )
            """)
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_snapshots_location ON price_snapshots(location)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_snapshots_date ON price_snapshots(pickup_date)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_snapshots_group ON price_snapshots(\"group\")")
            tables_created.append("price_snapshots")
            print("   ✅ price_snapshots criada")
        except Exception as e:
            print(f"   ⚠️  Erro: {e}")
            conn.rollback()
        
        # 2. user_settings
        print("2️⃣  Criando tabela user_settings...")
        try:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_settings (
                    user_key TEXT NOT NULL,
                    setting_key TEXT NOT NULL,
                    setting_value TEXT NOT NULL,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    PRIMARY KEY (user_key, setting_key)
                )
            """)
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_user_settings_user ON user_settings(user_key)")
            tables_created.append("user_settings")
            print("   ✅ user_settings criada")
        except Exception as e:
            print(f"   ⚠️  Erro: {e}")
            conn.rollback()
        
        # 3. search_history
        print("3️⃣  Criando tabela search_history...")
        try:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS search_history (
                    id SERIAL PRIMARY KEY,
                    location TEXT NOT NULL,
                    start_date TEXT NOT NULL,
                    end_date TEXT NOT NULL,
                    days INTEGER NOT NULL,
                    results_count INTEGER DEFAULT 0,
                    min_price REAL,
                    max_price REAL,
                    avg_price REAL,
                    "user" TEXT,
                    search_params TEXT,
                    search_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_search_history_location ON search_history(location)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_search_history_date ON search_history(search_timestamp)")
            tables_created.append("search_history")
            print("   ✅ search_history criada")
        except Exception as e:
            print(f"   ⚠️  Erro: {e}")
            conn.rollback()
        
        # 4. price_history
        print("4️⃣  Criando tabela price_history...")
        try:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS price_history (
                    id SERIAL PRIMARY KEY,
                    year INTEGER NOT NULL,
                    month INTEGER NOT NULL,
                    location TEXT NOT NULL,
                    prices_data TEXT NOT NULL,
                    saved_by TEXT,
                    saved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    history_type TEXT DEFAULT 'current_prices'
                )
            """)
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_price_history_date ON price_history(year, month)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_price_history_location ON price_history(location)")
            tables_created.append("price_history")
            print("   ✅ price_history criada")
        except Exception as e:
            print(f"   ⚠️  Erro: {e}")
            conn.rollback()
        
        # 5. automated_prices_history
        print("5️⃣  Criando tabela automated_prices_history...")
        try:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS automated_prices_history (
                    id SERIAL PRIMARY KEY,
                    year INTEGER NOT NULL,
                    month INTEGER NOT NULL,
                    location TEXT NOT NULL,
                    prices_data TEXT NOT NULL,
                    saved_by TEXT,
                    saved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_auto_history_date ON automated_prices_history(year, month)")
            tables_created.append("automated_prices_history")
            print("   ✅ automated_prices_history criada")
        except Exception as e:
            print(f"   ⚠️  Erro: {e}")
            conn.rollback()
        
        # 6. notification_rules
        print("6️⃣  Criando tabela notification_rules...")
        try:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS notification_rules (
                    id SERIAL PRIMARY KEY,
                    rule_name TEXT NOT NULL,
                    rule_type TEXT NOT NULL,
                    conditions TEXT NOT NULL,
                    recipients TEXT NOT NULL,
                    enabled BOOLEAN DEFAULT TRUE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            tables_created.append("notification_rules")
            print("   ✅ notification_rules criada")
        except Exception as e:
            print(f"   ⚠️  Erro: {e}")
            conn.rollback()
        
        # 7. notification_history
        print("7️⃣  Criando tabela notification_history...")
        try:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS notification_history (
                    id SERIAL PRIMARY KEY,
                    rule_id INTEGER,
                    notification_type TEXT NOT NULL,
                    recipient TEXT NOT NULL,
                    subject TEXT,
                    message TEXT,
                    sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    status TEXT DEFAULT 'sent'
                )
            """)
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_notif_history_date ON notification_history(sent_at)")
            tables_created.append("notification_history")
            print("   ✅ notification_history criada")
        except Exception as e:
            print(f"   ⚠️  Erro: {e}")
            conn.rollback()
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print()
        print("=" * 80)
        print(f"✅ {len(tables_created)} TABELAS CRIADAS COM SUCESSO!")
        print("=" * 80)
        print()
        
        for i, table in enumerate(tables_created, 1):
            print(f"   {i}. {table}")
        
        print()
        print("📋 Próximos passos:")
        print("   1. Reiniciar o serviço no Render")
        print("   2. Testar funcionalidades")
        print()
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao criar tabelas: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Executar fix"""
    print()
    print("🔧 FIX: Criar todas as tabelas em falta")
    print()
    
    success = create_all_tables()
    
    if success:
        print("✅ Todas as tabelas criadas!")
    else:
        print("❌ Erro ao criar tabelas!")
        print()
        print("💡 Dicas:")
        print("   1. Verificar se DATABASE_URL está configurado")
        print("   2. Verificar permissões do PostgreSQL")
        print("   3. Executar no Render Shell")
        print()

if __name__ == "__main__":
    main()
