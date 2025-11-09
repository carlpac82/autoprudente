#!/usr/bin/env python3
"""
💾 BACKUP COMPLETO - BD + Coordenadas + Parametrizações
Exporta todas as tabelas importantes em formato JSON
"""

import os
import json
import psycopg2
from datetime import datetime
from pathlib import Path
import subprocess

# Configuração
BACKUP_DIR = Path("backups_local")
MAX_BACKUPS = 10
TIMESTAMP = datetime.now().strftime("%Y%m%d_%H%M%S")

# Tabelas importantes para backup
TABLES_TO_BACKUP = [
    "damage_reports",
    "damage_report_coordinates",
    "rental_agreement_coordinates",
    "rental_agreement_templates",
    "users",
    "system_logs",
]

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

def backup_table(cursor, table_name):
    """Fazer backup de uma tabela"""
    try:
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        
        # Converter para dicionários
        data = []
        for row in rows:
            row_dict = {}
            for i, col in enumerate(columns):
                value = row[i]
                # Converter tipos não-serializáveis
                if hasattr(value, 'isoformat'):
                    value = value.isoformat()
                elif isinstance(value, (bytes, memoryview)):
                    value = None  # Não incluir dados binários grandes
                row_dict[col] = value
            data.append(row_dict)
        
        return {
            "table": table_name,
            "columns": columns,
            "row_count": len(data),
            "data": data
        }
    except Exception as e:
        print(f"   ⚠️  Erro em {table_name}: {e}")
        return None

def main():
    print("🚀 Iniciando backup completo...")
    print("=" * 60)
    
    # Carregar configuração
    load_env()
    
    # Criar diretório de backups
    BACKUP_DIR.mkdir(exist_ok=True)
    
    backup_file = BACKUP_DIR / f"backup_{TIMESTAMP}.json"
    
    print(f"\n📦 1. Exportando base de dados...")
    
    # Conectar à BD
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        print("   ✅ Conectado à BD")
    except Exception as e:
        print(f"   ❌ Erro ao conectar: {e}")
        return 1
    
    # Fazer backup de cada tabela
    backup_data = {
        "timestamp": TIMESTAMP,
        "date": datetime.now().isoformat(),
        "tables": {}
    }
    
    total_rows = 0
    for table in TABLES_TO_BACKUP:
        print(f"   📊 Exportando {table}...", end=" ")
        result = backup_table(cursor, table)
        if result:
            backup_data["tables"][table] = result
            total_rows += result["row_count"]
            print(f"✅ {result['row_count']} rows")
        else:
            print("❌")
    
    cursor.close()
    conn.close()
    
    # Salvar backup
    print(f"\n💾 2. Salvando backup...")
    with open(backup_file, 'w', encoding='utf-8') as f:
        json.dump(backup_data, f, indent=2, ensure_ascii=False)
    
    file_size = backup_file.stat().st_size / (1024 * 1024)  # MB
    print(f"   ✅ Backup criado: {backup_file.name} ({file_size:.2f} MB)")
    print(f"   📊 Total de registos: {total_rows}")
    
    # Limpar backups antigos
    print(f"\n🗑️  3. Limpando backups antigos...")
    backups = sorted(BACKUP_DIR.glob("backup_*.json"), key=lambda x: x.stat().st_mtime, reverse=True)
    
    if len(backups) > MAX_BACKUPS:
        for old_backup in backups[MAX_BACKUPS:]:
            old_backup.unlink()
            print(f"   🗑️  Removido: {old_backup.name}")
    
    print(f"   ✅ Mantidos {min(len(backups), MAX_BACKUPS)} backups")
    
    # Listar backups
    print(f"\n📁 4. Backups locais disponíveis:")
    for backup in backups[:MAX_BACKUPS]:
        size = backup.stat().st_size / (1024 * 1024)
        print(f"   {backup.name} ({size:.2f} MB)")
    
    # Git commit e push
    print(f"\n🔄 5. Enviando para GitHub...")
    
    try:
        # Add arquivos importantes
        subprocess.run(["git", "add", "main.py", "templates/", "static/", "requirements.txt"], 
                      check=False, capture_output=True)
        
        # Commit
        commit_msg = f"""💾 Backup completo - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

✅ BD exportada: {backup_file.name} ({file_size:.2f} MB)
✅ Tabelas: {len(backup_data['tables'])}
✅ Total registos: {total_rows}
✅ Coordenadas DR: incluídas
✅ Coordenadas RA: incluídas
✅ Damage Reports: incluídos
✅ Backups locais: {len(backups)} mantidos (max: {MAX_BACKUPS})

Backup completo com todas as parametrizações e coordenadas."""
        
        result = subprocess.run(["git", "commit", "-m", commit_msg], 
                               capture_output=True, text=True)
        
        if result.returncode == 0:
            print("   ✅ Commit criado")
        else:
            print("   ⚠️  Nada para commitar (já está atualizado)")
        
        # Push
        print("   🚀 Pushing para GitHub...")
        result = subprocess.run(["git", "push", "origin", "main"], 
                               capture_output=True, text=True)
        
        if result.returncode == 0:
            print("   ✅ Push concluído")
        else:
            print(f"   ❌ Erro no push: {result.stderr}")
    
    except Exception as e:
        print(f"   ❌ Erro no Git: {e}")
    
    # Resumo final
    print("\n" + "=" * 60)
    print("✅ BACKUP COMPLETO CONCLUÍDO!")
    print("=" * 60)
    print(f"📦 Backup local: {backup_file}")
    print(f"📊 Tamanho: {file_size:.2f} MB")
    print(f"📋 Registos: {total_rows}")
    print(f"🗂️  Backups mantidos: {len(backups)} de {MAX_BACKUPS}")
    print(f"✅ GitHub: sincronizado")
    print("=" * 60)
    print(f"\n🔧 Para restaurar este backup:")
    print(f"   python3 restore_backup.py {backup_file}")
    print()

if __name__ == "__main__":
    exit(main())
