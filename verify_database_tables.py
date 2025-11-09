#!/usr/bin/env python3
"""
🔍 VERIFICAR TABELAS E DADOS NA BASE DE DADOS POSTGRESQL

Verifica:
1. Tabelas existentes
2. Configurações automatedReportsAdvanced
3. Recent searches
4. OAuth tokens
"""

import os
import sys
from pathlib import Path

def load_env():
    """Load .env variables"""
    env_file = Path(".env")
    if env_file.exists():
        with open(env_file) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    if '=' in line:
                        key, value = line.split('=', 1)
                        os.environ[key] = value

def verify_database():
    """Verify database tables and data"""
    print("\n" + "="*80)
    print("🔍 VERIFICANDO BASE DE DADOS POSTGRESQL")
    print("="*80)
    
    load_env()
    
    database_url = os.environ.get('DATABASE_URL')
    if not database_url:
        print("❌ DATABASE_URL não encontrada no .env")
        return
    
    print(f"\n📊 Conectando à base de dados...")
    print(f"   URL: {database_url[:50]}...")
    
    try:
        import psycopg2
        conn = psycopg2.connect(database_url)
        cursor = conn.cursor()
        
        # 1. Verificar tabelas
        print("\n" + "="*80)
        print("1️⃣ TABELAS EXISTENTES:")
        print("="*80)
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name
        """)
        tables = cursor.fetchall()
        
        important_tables = [
            'recent_searches',
            'price_automation_settings',
            'oauth_tokens',
            'users'
        ]
        
        for table in tables:
            table_name = table[0]
            is_important = '✅' if table_name in important_tables else '  '
            print(f"{is_important} {table_name}")
        
        # 2. Verificar recent_searches
        print("\n" + "="*80)
        print("2️⃣ TABELA recent_searches:")
        print("="*80)
        cursor.execute("""
            SELECT COUNT(*) FROM recent_searches
        """)
        count = cursor.fetchone()[0]
        print(f"   Total registos: {count}")
        
        if count > 0:
            cursor.execute("""
                SELECT location, start_date, days, timestamp
                FROM recent_searches
                ORDER BY timestamp DESC
                LIMIT 10
            """)
            rows = cursor.fetchall()
            print(f"\n   Últimas 10 pesquisas:")
            for row in rows:
                location, start_date, days, timestamp = row
                print(f"   • {location} | {start_date} | {days}d | {timestamp}")
        else:
            print("   ⚠️ NENHUMA PESQUISA ENCONTRADA!")
            print("   → Sistema precisa executar pesquisas automáticas")
        
        # 3. Verificar price_automation_settings
        print("\n" + "="*80)
        print("3️⃣ TABELA price_automation_settings:")
        print("="*80)
        cursor.execute("""
            SELECT setting_key, LENGTH(setting_value) as size, updated_at
            FROM price_automation_settings
            ORDER BY updated_at DESC
        """)
        rows = cursor.fetchall()
        
        if rows:
            for row in rows:
                key, size, updated = row
                print(f"   • {key}: {size} chars | Updated: {updated}")
                
                # Se for automatedReportsAdvanced, mostrar conteúdo
                if key == 'automatedReportsAdvanced':
                    cursor.execute("""
                        SELECT setting_value
                        FROM price_automation_settings
                        WHERE setting_key = 'automatedReportsAdvanced'
                    """)
                    value_row = cursor.fetchone()
                    if value_row:
                        import json
                        settings = json.loads(value_row[0])
                        print(f"\n   📋 automatedReportsAdvanced:")
                        if settings.get('daily', {}).get('enabled'):
                            schedules = settings['daily'].get('schedules', [])
                            print(f"      Daily: {len(schedules)} schedules")
                            for idx, s in enumerate(schedules):
                                print(f"        #{idx+1}: {s.get('searchTime')} → {s.get('sendTime')}")
                                print(f"           Days: {s.get('days')}")
                                print(f"           Locations: {s.get('locations')}")
                        if settings.get('weekly', {}).get('enabled'):
                            print(f"      Weekly: ✅ Enabled")
                        if settings.get('monthly', {}).get('enabled'):
                            print(f"      Monthly: ✅ Enabled")
        else:
            print("   ⚠️ Nenhuma configuração encontrada!")
        
        # 4. Verificar oauth_tokens
        print("\n" + "="*80)
        print("4️⃣ TABELA oauth_tokens:")
        print("="*80)
        cursor.execute("""
            SELECT provider, user_email, 
                   CASE WHEN access_token IS NOT NULL AND access_token != '' THEN 'YES' ELSE 'NO' END as has_access,
                   CASE WHEN refresh_token IS NOT NULL AND refresh_token != '' THEN 'YES' ELSE 'NO' END as has_refresh,
                   updated_at
            FROM oauth_tokens
            WHERE provider = 'google'
            ORDER BY updated_at DESC
            LIMIT 1
        """)
        row = cursor.fetchone()
        
        if row:
            provider, email, has_access, has_refresh, updated = row
            print(f"   Email: {email}")
            print(f"   Access Token: {has_access}")
            print(f"   Refresh Token: {has_refresh}")
            print(f"   Updated: {updated}")
            
            if has_access == 'YES' and has_refresh == 'YES':
                print(f"\n   ✅ Gmail OAuth: FUNCIONAL")
            else:
                print(f"\n   ⚠️ Gmail OAuth: INCOMPLETO")
        else:
            print("   ❌ Nenhuma credencial Gmail encontrada!")
        
        # 5. Verificar estrutura recent_searches
        print("\n" + "="*80)
        print("5️⃣ ESTRUTURA DA TABELA recent_searches:")
        print("="*80)
        cursor.execute("""
            SELECT column_name, data_type, is_nullable
            FROM information_schema.columns
            WHERE table_name = 'recent_searches'
            ORDER BY ordinal_position
        """)
        columns = cursor.fetchall()
        
        for col in columns:
            col_name, data_type, nullable = col
            print(f"   • {col_name}: {data_type} (nullable: {nullable})")
        
        cursor.close()
        conn.close()
        
        print("\n" + "="*80)
        print("✅ VERIFICAÇÃO COMPLETA!")
        print("="*80)
        
    except Exception as e:
        print(f"\n❌ ERRO: {str(e)}")
        import traceback
        print(traceback.format_exc())

if __name__ == "__main__":
    verify_database()
