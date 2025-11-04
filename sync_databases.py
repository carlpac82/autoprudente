#!/usr/bin/env python3
"""
Script de Sincronização Bilateral entre Render (PostgreSQL) e Local (SQLite)
"""

import os
import sys
import subprocess
import sqlite3
from datetime import datetime
from pathlib import Path
import json

def check_pg_dump():
    """Verifica se pg_dump está instalado"""
    try:
        result = subprocess.run(["pg_dump", "--version"], capture_output=True, text=True)
        print(f"✅ pg_dump encontrado: {result.stdout.strip()}")
        return True
    except FileNotFoundError:
        print("❌ pg_dump não encontrado!")
        print("   Instale PostgreSQL: brew install postgresql@14")
        return False

def backup_render_postgres():
    """Faz backup do PostgreSQL do Render"""
    print("\n" + "="*80)
    print("🐘 BACKUP DO POSTGRESQL DO RENDER")
    print("="*80)
    
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        print("❌ DATABASE_URL não encontrada!")
        print("   Configure: export DATABASE_URL=postgresql://...")
        return None
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = f"render_backup_{timestamp}.sql"
    backup_path = Path("backups") / backup_file
    
    # Criar diretório
    backup_path.parent.mkdir(exist_ok=True)
    
    print(f"📥 A fazer backup do PostgreSQL...")
    print(f"   Ficheiro: {backup_file}")
    
    try:
        result = subprocess.run(
            ["pg_dump", db_url],
            capture_output=True,
            text=True,
            timeout=300  # 5 minutos
        )
        
        if result.returncode == 0:
            with open(backup_path, 'w') as f:
                f.write(result.stdout)
            
            size_mb = backup_path.stat().st_size / (1024 * 1024)
            print(f"✅ Backup criado: {size_mb:.2f} MB")
            return backup_path
        else:
            print(f"❌ Erro: {result.stderr}")
            return None
            
    except subprocess.TimeoutExpired:
        print("❌ Timeout! Backup demorou mais de 5 minutos")
        return None
    except Exception as e:
        print(f"❌ Erro: {e}")
        return None

def export_sqlite_to_sql():
    """Exporta SQLite local para SQL"""
    print("\n" + "="*80)
    print("📁 EXPORT DO SQLITE LOCAL")
    print("="*80)
    
    db_path = Path("data.db")
    if not db_path.exists():
        print("❌ data.db não encontrado!")
        return None
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    export_file = f"local_export_{timestamp}.sql"
    export_path = Path("backups") / export_file
    
    print(f"📤 A exportar SQLite...")
    print(f"   Ficheiro: {export_file}")
    
    try:
        result = subprocess.run(
            ["sqlite3", str(db_path), ".dump"],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if result.returncode == 0:
            with open(export_path, 'w') as f:
                f.write(result.stdout)
            
            size_mb = export_path.stat().st_size / (1024 * 1024)
            print(f"✅ Export criado: {size_mb:.2f} MB")
            return export_path
        else:
            print(f"❌ Erro: {result.stderr}")
            return None
            
    except Exception as e:
        print(f"❌ Erro: {e}")
        return None

def compare_databases():
    """Compara estrutura e dados entre local e Render"""
    print("\n" + "="*80)
    print("🔍 COMPARAÇÃO DE BASES DE DADOS")
    print("="*80)
    
    # Contar registos local
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
    tables = [row[0] for row in cursor.fetchall()]
    
    local_stats = {}
    for table in tables:
        try:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            local_stats[table] = count
        except:
            local_stats[table] = 0
    
    conn.close()
    
    print("\n📊 Estatísticas Local (SQLite):")
    total_local = 0
    for table, count in sorted(local_stats.items()):
        if count > 0:
            print(f"   {table}: {count:,} registos")
            total_local += count
    
    print(f"\n   TOTAL: {total_local:,} registos")
    
    # TODO: Comparar com PostgreSQL (requer conexão)
    print("\n⚠️ Comparação com PostgreSQL requer DATABASE_URL configurada")
    
    return local_stats

def sync_render_to_local():
    """Sincroniza PostgreSQL do Render para SQLite local"""
    print("\n" + "="*80)
    print("🔄 SINCRONIZAÇÃO: RENDER → LOCAL")
    print("="*80)
    
    # 1. Backup do Render
    backup_path = backup_render_postgres()
    if not backup_path:
        return False
    
    # 2. Backup do local atual
    print("\n📦 A fazer backup do local atual...")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    local_backup = Path(f"data_backup_{timestamp}.db")
    
    import shutil
    shutil.copy2("data.db", local_backup)
    print(f"✅ Backup local: {local_backup}")
    
    # 3. Converter PostgreSQL para SQLite
    print("\n🔄 A converter PostgreSQL para SQLite...")
    print("⚠️ AVISO: Conversão automática não implementada!")
    print("   Opções:")
    print("   1. Usar ferramenta: pgloader")
    print("   2. Usar script Python personalizado")
    print("   3. Importar manualmente")
    
    return True

def sync_local_to_render():
    """Sincroniza SQLite local para PostgreSQL do Render"""
    print("\n" + "="*80)
    print("🔄 SINCRONIZAÇÃO: LOCAL → RENDER")
    print("="*80)
    
    print("⚠️ AVISO: Esta operação vai SOBRESCREVER dados no Render!")
    print("   Tem certeza? (y/N): ", end='')
    
    response = input().strip().lower()
    if response != 'y':
        print("❌ Cancelado")
        return False
    
    # 1. Export do local
    export_path = export_sqlite_to_sql()
    if not export_path:
        return False
    
    # 2. Converter para PostgreSQL
    print("\n🔄 A converter SQLite para PostgreSQL...")
    print("⚠️ AVISO: Conversão automática não implementada!")
    print("   Requer conversão manual de:")
    print("   - AUTOINCREMENT → SERIAL")
    print("   - BLOB → BYTEA")
    print("   - Placeholders ? → %s")
    
    return True

def create_sync_report():
    """Cria relatório de sincronização"""
    print("\n" + "="*80)
    print("📋 RELATÓRIO DE SINCRONIZAÇÃO")
    print("="*80)
    
    report = {
        "timestamp": datetime.now().isoformat(),
        "local_db": str(Path("data.db").absolute()),
        "local_size_mb": Path("data.db").stat().st_size / (1024 * 1024) if Path("data.db").exists() else 0,
        "render_url": os.getenv("DATABASE_URL", "Not configured"),
        "backups_dir": str(Path("backups").absolute()),
    }
    
    # Contar backups
    backups_dir = Path("backups")
    if backups_dir.exists():
        render_backups = list(backups_dir.glob("render_backup_*.sql"))
        local_backups = list(backups_dir.glob("local_export_*.sql"))
        
        report["render_backups_count"] = len(render_backups)
        report["local_backups_count"] = len(local_backups)
        
        if render_backups:
            latest = max(render_backups, key=lambda p: p.stat().st_mtime)
            report["latest_render_backup"] = {
                "file": latest.name,
                "size_mb": latest.stat().st_size / (1024 * 1024),
                "date": datetime.fromtimestamp(latest.stat().st_mtime).isoformat()
            }
    
    # Guardar relatório
    report_file = Path("backups") / f"sync_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(report_file, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\n✅ Relatório guardado: {report_file}")
    
    # Mostrar resumo
    print("\n📊 Resumo:")
    print(f"   Local DB: {report['local_size_mb']:.2f} MB")
    print(f"   Render URL: {'Configurado' if 'postgresql' in report['render_url'] else 'Não configurado'}")
    print(f"   Backups Render: {report.get('render_backups_count', 0)}")
    print(f"   Backups Local: {report.get('local_backups_count', 0)}")
    
    return report

def main():
    """Menu principal"""
    print("\n" + "="*80)
    print("🔄 SINCRONIZAÇÃO DE BASES DE DADOS")
    print("   Render (PostgreSQL) ↔ Local (SQLite)")
    print("="*80)
    
    # Verificar requisitos
    if not check_pg_dump():
        sys.exit(1)
    
    while True:
        print("\n📋 OPÇÕES:")
        print("   1. Backup do PostgreSQL do Render")
        print("   2. Export do SQLite local")
        print("   3. Comparar bases de dados")
        print("   4. Sincronizar Render → Local")
        print("   5. Sincronizar Local → Render")
        print("   6. Criar relatório")
        print("   0. Sair")
        print("\nEscolha: ", end='')
        
        choice = input().strip()
        
        if choice == '1':
            backup_render_postgres()
        elif choice == '2':
            export_sqlite_to_sql()
        elif choice == '3':
            compare_databases()
        elif choice == '4':
            sync_render_to_local()
        elif choice == '5':
            sync_local_to_render()
        elif choice == '6':
            create_sync_report()
        elif choice == '0':
            print("\n👋 Até logo!")
            break
        else:
            print("❌ Opção inválida!")

if __name__ == '__main__':
    main()
