"""
Script para verificar TODOS os dados armazenados no PostgreSQL
"""

import psycopg2
import os
from datetime import datetime

DATABASE_URL = os.environ.get('DATABASE_URL') or "postgresql://carrental_user:cmXcauHIuQinAyDQjcB9XiVMU0Gaxviz@dpg-d44gvnm3jp1c73dc2edg-a.frankfurt-postgres.render.com/carrental_db_9klo?sslmode=require"

def check_table_data(cursor, table_name):
    """Verifica quantos registos existem numa tabela"""
    try:
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        count = cursor.fetchone()[0]
        return count
    except Exception as e:
        return f"ERROR: {str(e)}"

try:
    print("=" * 80)
    print("🔍 VERIFICAÇÃO COMPLETA DE ARMAZENAMENTO DE DADOS NO POSTGRESQL")
    print("=" * 80)
    print(f"📅 Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    
    # Listar todas as tabelas
    cursor.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public' 
        ORDER BY table_name
    """)
    
    tables = [row[0] for row in cursor.fetchall()]
    
    print(f"📊 Total de tabelas encontradas: {len(tables)}\n")
    print("=" * 80)
    
    # Categorias de dados
    categories = {
        "👥 UTILIZADORES E AUTENTICAÇÃO": [
            "users", "activity_log", "oauth_tokens"
        ],
        "🚗 VEÍCULOS E FOTOS": [
            "vehicle_photos", "vehicle_images", "vehicle_name_overrides", "car_images", "car_groups"
        ],
        "💰 PREÇOS E AUTOMAÇÃO": [
            "price_snapshots", "automated_price_rules", "pricing_strategies", 
            "automated_prices_history", "price_automation_settings", "vans_pricing"
        ],
        "🤖 AI E APRENDIZAGEM": [
            "ai_learning_data"
        ],
        "📊 HISTÓRICOS E PESQUISAS": [
            "search_history", "export_history"
        ],
        "📧 EMAIL E NOTIFICAÇÕES": [
            "notification_rules", "notification_history"
        ],
        "📄 DAMAGE REPORTS": [
            "damage_reports", "damage_report_coordinates", "damage_report_mapping_history",
            "damage_report_templates", "damage_report_numbering"
        ],
        "⚙️ SISTEMA E CACHE": [
            "system_logs", "cache_data", "file_storage", "user_settings", "custom_days", "app_settings"
        ]
    }
    
    total_records = 0
    empty_tables = []
    
    for category, table_list in categories.items():
        print(f"\n{category}")
        print("-" * 80)
        
        for table in table_list:
            if table in tables:
                count = check_table_data(cursor, table)
                if isinstance(count, int):
                    total_records += count
                    status = "✅" if count > 0 else "⚠️ VAZIA"
                    if count == 0:
                        empty_tables.append(table)
                    print(f"  {status} {table:<40} {count:>10} registos")
                else:
                    print(f"  ❌ {table:<40} {count}")
            else:
                print(f"  ❌ {table:<40} TABELA NÃO EXISTE")
    
    # Tabelas não categorizadas
    other_tables = [t for t in tables if not any(t in cat_tables for cat_tables in categories.values())]
    if other_tables:
        print(f"\n📦 OUTRAS TABELAS")
        print("-" * 80)
        for table in other_tables:
            count = check_table_data(cursor, table)
            if isinstance(count, int):
                total_records += count
                status = "✅" if count > 0 else "⚠️"
                if count == 0:
                    empty_tables.append(table)
                print(f"  {status} {table:<40} {count:>10} registos")
    
    # Resumo
    print("\n" + "=" * 80)
    print("📈 RESUMO FINAL")
    print("=" * 80)
    print(f"Total de tabelas: {len(tables)}")
    print(f"Total de registos: {total_records:,}")
    print(f"Tabelas com dados: {len(tables) - len(empty_tables)}")
    print(f"Tabelas vazias: {len(empty_tables)}")
    
    if empty_tables:
        print(f"\n⚠️ Tabelas vazias (ainda não utilizadas):")
        for table in empty_tables:
            print(f"  - {table}")
    
    # Verificar dados críticos
    print("\n" + "=" * 80)
    print("🔍 VERIFICAÇÃO DE DADOS CRÍTICOS")
    print("=" * 80)
    
    critical_checks = [
        ("Utilizadores cadastrados", "SELECT COUNT(*) FROM users"),
        ("Fotos de veículos", "SELECT COUNT(*) FROM vehicle_photos WHERE photo_data IS NOT NULL"),
        ("Snapshots de preços", "SELECT COUNT(*) FROM price_snapshots"),
        ("Regras de automação", "SELECT COUNT(*) FROM automated_price_rules"),
        ("Estratégias de pricing", "SELECT COUNT(*) FROM pricing_strategies"),
        ("Damage Reports", "SELECT COUNT(*) FROM damage_reports"),
        ("Coordenadas DR mapeadas", "SELECT COUNT(*) FROM damage_report_coordinates"),
        ("Tokens OAuth (Gmail)", "SELECT COUNT(*) FROM oauth_tokens"),
    ]
    
    for check_name, query in critical_checks:
        try:
            cursor.execute(query)
            count = cursor.fetchone()[0]
            status = "✅" if count > 0 else "⚠️ NENHUM"
            print(f"{status} {check_name:<35} {count:>10}")
        except Exception as e:
            print(f"❌ {check_name:<35} ERROR: {str(e)}")
    
    cursor.close()
    conn.close()
    
    print("\n" + "=" * 80)
    print("✅ VERIFICAÇÃO CONCLUÍDA!")
    print("=" * 80)
    
except Exception as e:
    print(f"❌ Erro na conexão: {e}")
    import traceback
    traceback.print_exc()
