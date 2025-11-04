#!/usr/bin/env python3
"""
Fix PostgreSQL Schema - Para executar no Render Shell
Copiar e colar TODO este ficheiro no Shell
"""

# Copiar e colar TODO este código no Render Shell:
# python3 -c "$(cat << 'ENDOFPYTHON'

import os
import sys

# Verificar se database.py existe
try:
    from database import _db_connect, USE_POSTGRES
    print("✅ database.py importado")
except ImportError:
    print("❌ database.py não encontrado")
    print("Tentando importar psycopg2 diretamente...")
    try:
        import psycopg2
        from urllib.parse import urlparse
        
        DATABASE_URL = os.getenv("DATABASE_URL")
        if not DATABASE_URL:
            print("❌ DATABASE_URL não encontrado")
            sys.exit(1)
        
        print(f"✅ DATABASE_URL encontrado")
        result = urlparse(DATABASE_URL)
        
        print(f"📊 Conectando ao PostgreSQL...")
        print(f"   Host: {result.hostname}")
        print(f"   Database: {result.path[1:]}")
        
        conn = psycopg2.connect(DATABASE_URL)
        conn.autocommit = True
        cursor = conn.cursor()
        
        print(f"\n✅ Conectado!")
        
        columns = [
            ("first_name", "TEXT"),
            ("last_name", "TEXT"),
            ("email", "TEXT"),
            ("mobile", "TEXT"),
            ("profile_picture_path", "TEXT"),
            ("is_admin", "INTEGER DEFAULT 0"),
            ("enabled", "INTEGER DEFAULT 1"),
            ("created_at", "TEXT"),
            ("google_id", "TEXT"),
        ]
        
        print(f"\n🔧 Adicionando colunas faltantes...")
        for col_name, col_type in columns:
            try:
                cursor.execute(f"ALTER TABLE users ADD COLUMN IF NOT EXISTS {col_name} {col_type}")
                print(f"   ✅ {col_name}")
            except Exception as e:
                if "already exists" in str(e):
                    print(f"   ✓ {col_name} (já existe)")
                else:
                    print(f"   ❌ {col_name}: {e}")
        
        print(f"\n📋 Verificando schema...")
        cursor.execute("SELECT column_name FROM information_schema.columns WHERE table_name='users' ORDER BY ordinal_position")
        cols = [row[0] for row in cursor.fetchall()]
        
        print(f"   Total de colunas: {len(cols)}")
        print(f"   Colunas: {', '.join(cols)}")
        
        if 'enabled' in cols:
            print(f"\n✅ SUCESSO! Coluna 'enabled' existe!")
        else:
            print(f"\n❌ ERRO: Coluna 'enabled' ainda não existe!")
        
        cursor.close()
        conn.close()
        
        print(f"\n{'='*60}")
        print(f"✅ SCHEMA CORRIGIDO!")
        print(f"{'='*60}")
        
    except Exception as e:
        print(f"\n❌ ERRO: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

# ENDOFPYTHON
# )"
