#!/usr/bin/env python3
"""
Fix PostgreSQL Schema on Render
Adiciona colunas faltantes na tabela users
"""
import os
import sys

# Verificar se está no Render
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    print("❌ DATABASE_URL não encontrado")
    print("Este script deve ser executado no Render Shell")
    sys.exit(1)

print("=" * 60)
print("🔧 FIXING POSTGRESQL SCHEMA ON RENDER")
print("=" * 60)

try:
    import psycopg2
    from urllib.parse import urlparse
    
    # Parse DATABASE_URL
    result = urlparse(DATABASE_URL)
    
    print(f"📊 Conectando ao PostgreSQL...")
    print(f"   Host: {result.hostname}")
    print(f"   Database: {result.path[1:]}")
    
    # Conectar
    conn = psycopg2.connect(DATABASE_URL)
    conn.autocommit = False
    cursor = conn.cursor()
    
    print(f"\n✅ Conectado!")
    
    # Verificar colunas existentes
    print(f"\n📋 Verificando schema da tabela users...")
    cursor.execute("""
        SELECT column_name, data_type 
        FROM information_schema.columns 
        WHERE table_name = 'users'
        ORDER BY ordinal_position
    """)
    
    existing_columns = {row[0]: row[1] for row in cursor.fetchall()}
    print(f"   Colunas existentes: {len(existing_columns)}")
    for col, dtype in existing_columns.items():
        print(f"   - {col} ({dtype})")
    
    # Colunas necessárias
    required_columns = {
        'first_name': 'TEXT',
        'last_name': 'TEXT',
        'email': 'TEXT',
        'mobile': 'TEXT',
        'profile_picture_path': 'TEXT',
        'is_admin': 'INTEGER DEFAULT 0',
        'enabled': 'INTEGER DEFAULT 1',
        'created_at': 'TEXT',
        'google_id': 'TEXT UNIQUE'
    }
    
    print(f"\n🔧 Adicionando colunas faltantes...")
    
    changes_made = False
    for col_name, col_type in required_columns.items():
        if col_name not in existing_columns:
            try:
                # Começar nova transação
                if changes_made:
                    conn.commit()
                
                sql = f"ALTER TABLE users ADD COLUMN {col_name} {col_type}"
                print(f"   Adicionando: {col_name}...")
                cursor.execute(sql)
                conn.commit()
                print(f"   ✅ {col_name} adicionada")
                changes_made = True
                
            except Exception as e:
                conn.rollback()
                if "already exists" in str(e):
                    print(f"   ⚠️  {col_name} já existe")
                else:
                    print(f"   ❌ Erro ao adicionar {col_name}: {e}")
        else:
            print(f"   ✓ {col_name} já existe")
    
    # Verificar novamente
    print(f"\n📋 Verificando schema final...")
    cursor.execute("""
        SELECT column_name, data_type 
        FROM information_schema.columns 
        WHERE table_name = 'users'
        ORDER BY ordinal_position
    """)
    
    final_columns = {row[0]: row[1] for row in cursor.fetchall()}
    print(f"   Total de colunas: {len(final_columns)}")
    
    # Verificar se todas as colunas necessárias existem
    missing = []
    for col in required_columns.keys():
        if col not in final_columns:
            missing.append(col)
    
    if missing:
        print(f"\n⚠️  Colunas ainda faltando: {', '.join(missing)}")
    else:
        print(f"\n✅ Todas as colunas necessárias existem!")
    
    cursor.close()
    conn.close()
    
    print(f"\n{'='*60}")
    print(f"✅ SCHEMA CORRIGIDO COM SUCESSO!")
    print(f"{'='*60}")
    
except ImportError:
    print("❌ psycopg2 não instalado")
    print("Execute: pip install psycopg2-binary")
    sys.exit(1)
    
except Exception as e:
    print(f"\n❌ ERRO: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
