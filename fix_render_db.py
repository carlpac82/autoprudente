#!/usr/bin/env python3
"""
Script URGENTE para adicionar coluna downloaded_at na tabela vehicle_images
Executar ANTES de tentar fazer backup
"""

import os
import sys

try:
    import psycopg2
except ImportError:
    print("❌ psycopg2 não instalado!")
    print("💡 Instale com: pip install psycopg2-binary")
    sys.exit(1)

# Obter DATABASE_URL
DATABASE_URL = os.environ.get('DATABASE_URL')

if not DATABASE_URL:
    try:
        from dotenv import load_dotenv
        load_dotenv()
        DATABASE_URL = os.environ.get('DATABASE_URL')
    except:
        pass

if not DATABASE_URL:
    print("❌ DATABASE_URL não encontrada!")
    print("💡 Obter do Render Dashboard:")
    print("   1. https://dashboard.render.com")
    print("   2. Ir para serviço carrental-api")
    print("   3. Environment > DATABASE_URL")
    print("\nExemplo:")
    print("export DATABASE_URL='postgresql://user:pass@host:5432/dbname'")
    sys.exit(1)

print("=" * 70)
print("🔧 FIX URGENTE: Adicionar coluna downloaded_at")
print("=" * 70)
print(f"\n🔗 Conectando ao Render PostgreSQL...")

try:
    conn = psycopg2.connect(DATABASE_URL)
    print("✅ Conectado!")
except Exception as e:
    print(f"❌ Erro ao conectar: {e}")
    sys.exit(1)

try:
    with conn.cursor() as cur:
        # Verificar se coluna já existe
        cur.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name='vehicle_images' 
            AND column_name='downloaded_at'
        """)
        
        exists = cur.fetchone()
        
        if exists:
            print("\n✅ Coluna downloaded_at já existe!")
        else:
            print("\n⚙️  Adicionando coluna downloaded_at...")
            cur.execute("""
                ALTER TABLE vehicle_images 
                ADD COLUMN downloaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            """)
            conn.commit()
            print("✅ Coluna downloaded_at adicionada com sucesso!")
        
        # Verificar estrutura da tabela
        print("\n📋 Estrutura atual da tabela vehicle_images:")
        cur.execute("""
            SELECT column_name, data_type, is_nullable, column_default
            FROM information_schema.columns 
            WHERE table_name='vehicle_images'
            ORDER BY ordinal_position
        """)
        
        for row in cur.fetchall():
            print(f"   • {row[0]:20} {row[1]:20} NULL={row[2]:5} DEFAULT={row[3] or 'None'}")
        
        # Contar registos
        cur.execute("SELECT COUNT(*) FROM vehicle_images")
        count = cur.fetchone()[0]
        print(f"\n📊 Total de imagens na tabela: {count}")
        
    print("\n" + "=" * 70)
    print("✅ FIX COMPLETO!")
    print("=" * 70)
    print("\n💡 Agora podes fazer backup das fotos:")
    print("   python3 backup_photos_via_api.py")
    print("=" * 70)
    
except Exception as e:
    print(f"\n❌ ERRO: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
finally:
    conn.close()
    print("\n🔌 Conexão fechada")
