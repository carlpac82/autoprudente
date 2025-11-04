#!/usr/bin/env python3
"""
Script de Verificação da Base de Dados
Verifica todas as tabelas e dados guardados
"""
import sqlite3
from pathlib import Path
from datetime import datetime

print("=" * 80)
print("🔍 VERIFICAÇÃO DA BASE DE DADOS")
print("=" * 80)

# Verificar ficheiros de base de dados
db_files = ["data.db", "rental_tracker.db", "car_images.db", "carrental.db"]

for db_file in db_files:
    db_path = Path(db_file)
    
    if not db_path.exists():
        print(f"\n❌ {db_file} - NÃO EXISTE")
        continue
    
    size_kb = db_path.stat().st_size / 1024
    print(f"\n✅ {db_file} - {size_kb:.1f} KB")
    
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        
        # Listar todas as tabelas
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
        tables = cursor.fetchall()
        
        print(f"   📊 Tabelas: {len(tables)}")
        
        for (table_name,) in tables:
            # Contar registos
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                count = cursor.fetchone()[0]
                
                # Obter tamanho da tabela
                cursor.execute(f"SELECT SUM(pgsize) FROM dbstat WHERE name=?", (table_name,))
                size_result = cursor.fetchone()
                table_size = size_result[0] if size_result and size_result[0] else 0
                table_size_kb = table_size / 1024 if table_size else 0
                
                status = "✅" if count > 0 else "⚪"
                print(f"   {status} {table_name}: {count} registos ({table_size_kb:.1f} KB)")
                
            except Exception as e:
                print(f"   ❌ {table_name}: Erro ao contar - {e}")
        
        conn.close()
        
    except Exception as e:
        print(f"   ❌ Erro ao abrir: {e}")

# Verificar ficheiros uploaded
print(f"\n{'='*80}")
print("📁 FICHEIROS UPLOADED")
print("=" * 80)

uploads_dir = Path("uploads")
if uploads_dir.exists():
    files = list(uploads_dir.rglob("*"))
    file_count = len([f for f in files if f.is_file()])
    total_size = sum(f.stat().st_size for f in files if f.is_file())
    total_size_mb = total_size / (1024 * 1024)
    
    print(f"✅ Uploads: {file_count} ficheiros ({total_size_mb:.2f} MB)")
    
    # Listar ficheiros
    for file_path in sorted(files):
        if file_path.is_file():
            size_kb = file_path.stat().st_size / 1024
            print(f"   📄 {file_path.relative_to(uploads_dir)} ({size_kb:.1f} KB)")
else:
    print("❌ Pasta uploads não existe")

# Verificar backups
print(f"\n{'='*80}")
print("💾 BACKUPS")
print("=" * 80)

backup_dir = Path("backups")
if backup_dir.exists():
    backups = sorted(backup_dir.glob("*.zip"), key=lambda p: p.stat().st_mtime, reverse=True)
    
    print(f"✅ Backups: {len(backups)} ficheiros")
    
    for backup in backups[:5]:  # Mostrar últimos 5
        size_mb = backup.stat().st_size / (1024 * 1024)
        mtime = datetime.fromtimestamp(backup.stat().st_mtime)
        print(f"   💾 {backup.name} ({size_mb:.2f} MB) - {mtime.strftime('%Y-%m-%d %H:%M')}")
else:
    print("❌ Pasta backups não existe")

# Verificar PostgreSQL
print(f"\n{'='*80}")
print("🐘 POSTGRESQL")
print("=" * 80)

import os
DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL:
    print(f"✅ DATABASE_URL configurado")
    
    # Tentar conectar
    try:
        import psycopg2
        from urllib.parse import urlparse
        
        result = urlparse(DATABASE_URL)
        print(f"   Host: {result.hostname}")
        print(f"   Database: {result.path[1:]}")
        print(f"   User: {result.username}")
        
        # Testar conexão
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        
        # Listar tabelas
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name
        """)
        tables = cursor.fetchall()
        
        print(f"   📊 Tabelas PostgreSQL: {len(tables)}")
        
        for (table_name,) in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cursor.fetchone()[0]
            status = "✅" if count > 0 else "⚪"
            print(f"   {status} {table_name}: {count} registos")
        
        conn.close()
        print(f"\n✅ Conexão PostgreSQL OK")
        
    except ImportError:
        print("⚠️  psycopg2 não instalado")
    except Exception as e:
        print(f"❌ Erro ao conectar: {e}")
else:
    print("⚪ DATABASE_URL não configurado (modo local)")

print(f"\n{'='*80}")
print("✅ VERIFICAÇÃO COMPLETA")
print("=" * 80)
