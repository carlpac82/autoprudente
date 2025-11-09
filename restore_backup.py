#!/usr/bin/env python3
"""
🔧 RESTAURAR BACKUP COMPLETO
Restaura backup JSON criado pelo backup_full.py
"""

import os
import json
import sys
import psycopg2
from pathlib import Path
from datetime import datetime

def load_env():
    """Carregar .env"""
    env_file = Path(".env")
    if env_file.exists():
        with open(env_file) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    key, value = line.split('=', 1)
                    os.environ[key] = value

def get_db_connection():
    """Conectar à BD"""
    database_url = os.environ.get('DATABASE_URL')
    if not database_url:
        raise ValueError("DATABASE_URL não definida!")
    return psycopg2.connect(database_url)

def restore_table(cursor, table_data, dry_run=False):
    """Restaurar uma tabela"""
    table_name = table_data['table']
    rows = table_data['data']
    columns = table_data['columns']
    
    if not rows:
        print(f"   ⚠️  {table_name}: tabela vazia, a saltar")
        return 0
    
    # Preparar INSERT statement
    placeholders = ', '.join(['%s'] * len(columns))
    cols_str = ', '.join([f'"{col}"' for col in columns])
    insert_sql = f'INSERT INTO {table_name} ({cols_str}) VALUES ({placeholders})'
    
    # Contar registos existentes
    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
    existing_count = cursor.fetchone()[0]
    
    if dry_run:
        print(f"   🔍 {table_name}: {len(rows)} rows no backup, {existing_count} existentes")
        return len(rows)
    
    # Perguntar se quer limpar tabela
    if existing_count > 0:
        response = input(f"   ⚠️  {table_name} tem {existing_count} registos. Apagar? [s/N]: ")
        if response.lower() == 's':
            cursor.execute(f"DELETE FROM {table_name}")
            print(f"   🗑️  {existing_count} registos apagados")
    
    # Inserir dados
    inserted = 0
    errors = 0
    
    for row in rows:
        try:
            values = [row[col] for col in columns]
            cursor.execute(insert_sql, values)
            inserted += 1
            
            if inserted % 100 == 0:
                print(f"      {inserted}/{len(rows)} rows...", end='\r')
        except Exception as e:
            errors += 1
            if errors <= 3:  # Mostrar apenas primeiros 3 erros
                print(f"\n   ⚠️  Erro no registo {inserted + 1}: {str(e)[:100]}")
    
    print(f"   ✅ {table_name}: {inserted} rows inseridas", end="")
    if errors > 0:
        print(f" ({errors} erros)")
    else:
        print()
    
    return inserted

def main():
    if len(sys.argv) < 2:
        print("❌ Uso: python3 restore_backup.py <ficheiro_backup.json> [--dry-run]")
        print("\nBackups disponíveis:")
        backups_dir = Path("backups_local")
        if backups_dir.exists():
            for backup in sorted(backups_dir.glob("backup_*.json"), reverse=True)[:5]:
                size = backup.stat().st_size / (1024 * 1024)
                print(f"  • {backup.name} ({size:.2f} MB)")
        return 1
    
    backup_file = Path(sys.argv[1])
    dry_run = '--dry-run' in sys.argv
    
    if not backup_file.exists():
        print(f"❌ Ficheiro não encontrado: {backup_file}")
        return 1
    
    print("🔧 Iniciando restauração de backup...")
    print("=" * 60)
    print(f"📦 Backup: {backup_file}")
    
    if dry_run:
        print("🔍 MODO DRY-RUN (não faz alterações)")
    
    print()
    
    # Carregar configuração
    load_env()
    
    # Carregar backup
    print("📂 1. Carregando backup...")
    try:
        with open(backup_file, 'r', encoding='utf-8') as f:
            backup_data = json.load(f)
        
        backup_date = backup_data.get('date', 'desconhecido')
        tables_count = len(backup_data.get('tables', {}))
        
        print(f"   ✅ Backup de: {backup_date}")
        print(f"   📊 Tabelas: {tables_count}")
    except Exception as e:
        print(f"   ❌ Erro ao carregar: {e}")
        return 1
    
    # Conectar à BD
    print("\n🔌 2. Conectando à base de dados...")
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        print("   ✅ Conectado")
    except Exception as e:
        print(f"   ❌ Erro ao conectar: {e}")
        return 1
    
    # Restaurar tabelas
    print("\n📥 3. Restaurando tabelas...")
    
    if not dry_run:
        print("\n⚠️  AVISO: Esta operação irá modificar a base de dados!")
        response = input("Continuar? [s/N]: ")
        if response.lower() != 's':
            print("❌ Cancelado pelo utilizador")
            return 0
        print()
    
    total_restored = 0
    
    for table_name, table_data in backup_data.get('tables', {}).items():
        try:
            rows_restored = restore_table(cursor, table_data, dry_run)
            total_restored += rows_restored
        except Exception as e:
            print(f"   ❌ Erro em {table_name}: {e}")
    
    # Commit ou rollback
    if not dry_run:
        print("\n💾 4. Guardando alterações...")
        try:
            conn.commit()
            print("   ✅ Alterações guardadas")
        except Exception as e:
            print(f"   ❌ Erro ao guardar: {e}")
            conn.rollback()
            print("   🔄 Rollback efetuado")
    
    cursor.close()
    conn.close()
    
    # Resumo
    print("\n" + "=" * 60)
    if dry_run:
        print("✅ DRY-RUN CONCLUÍDO!")
    else:
        print("✅ RESTAURAÇÃO CONCLUÍDA!")
    print("=" * 60)
    print(f"📦 Backup: {backup_file.name}")
    print(f"📊 Tabelas: {tables_count}")
    print(f"📋 Registos: {total_restored}")
    
    if dry_run:
        print("\n💡 Para executar a restauração:")
        print(f"   python3 restore_backup.py {backup_file}")
    
    print("=" * 60)
    return 0

if __name__ == "__main__":
    try:
        exit(main())
    except KeyboardInterrupt:
        print("\n\n❌ Cancelado pelo utilizador")
        exit(1)
    except Exception as e:
        print(f"\n\n❌ Erro fatal: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
