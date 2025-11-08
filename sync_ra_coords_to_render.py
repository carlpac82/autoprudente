#!/usr/bin/env python3
"""
Script para copiar coordenadas do RA do SQLite local para PostgreSQL do Render
"""

import sqlite3
import psycopg2
import os
from datetime import datetime

# URL do PostgreSQL (colocar aqui ou usar variável de ambiente)
DATABASE_URL = os.getenv('DATABASE_URL') or input("Cole a DATABASE_URL do Render: ")

print("🔄 SINCRONIZAÇÃO DE COORDENADAS RA: SQLite → PostgreSQL")
print("="*60)

try:
    # 1. Ler coordenadas do SQLite local
    print("\n📥 Lendo coordenadas do SQLite local...")
    local_conn = sqlite3.connect('data.db')
    local_cursor = local_conn.execute("""
        SELECT field_id, x, y, width, height, page, field_type, template_version
        FROM rental_agreement_coordinates
        ORDER BY field_id
    """)
    coords = local_cursor.fetchall()
    local_conn.close()
    
    print(f"   ✅ Encontradas {len(coords)} coordenadas no SQLite local")
    
    if not coords:
        print("\n❌ ERRO: Nenhuma coordenada encontrada no SQLite local!")
        print("   💡 Certifique-se de ter mapeado os campos no localhost primeiro")
        exit(1)
    
    # Mostrar campos encontrados
    print("\n📋 Campos encontrados:")
    for row in coords:
        print(f"   • {row[0]:<20} (x={row[1]:.1f}, y={row[2]:.1f})")
    
    # 2. Conectar ao PostgreSQL do Render
    print(f"\n📤 Conectando ao PostgreSQL do Render...")
    pg_conn = psycopg2.connect(DATABASE_URL)
    pg_cur = pg_conn.cursor()
    
    print("   ✅ Conectado com sucesso!")
    
    # 3. Verificar se tabela existe
    pg_cur.execute("""
        SELECT EXISTS (
            SELECT FROM information_schema.tables 
            WHERE table_name = 'rental_agreement_coordinates'
        )
    """)
    table_exists = pg_cur.fetchone()[0]
    
    if not table_exists:
        print("\n❌ ERRO: Tabela rental_agreement_coordinates não existe no PostgreSQL!")
        print("   💡 Faça upload de um template primeiro no Render para criar a tabela")
        exit(1)
    
    # 4. Limpar coordenadas antigas (se existirem)
    print("\n🗑️  Limpando coordenadas antigas do PostgreSQL...")
    pg_cur.execute("DELETE FROM rental_agreement_coordinates")
    deleted = pg_cur.rowcount
    print(f"   ✅ Removidas {deleted} coordenadas antigas")
    
    # 5. Inserir coordenadas do SQLite
    print("\n💾 Inserindo coordenadas no PostgreSQL...")
    inserted = 0
    
    for row in coords:
        field_id, x, y, width, height, page, field_type, template_version = row
        
        pg_cur.execute("""
            INSERT INTO rental_agreement_coordinates 
            (field_id, x, y, width, height, page, field_type, template_version, created_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (field_id, x, y, width, height, page, field_type, template_version or 1, datetime.now()))
        
        inserted += 1
        print(f"   ✅ {field_id}")
    
    # 6. Commit
    pg_conn.commit()
    
    print(f"\n🎉 SUCESSO! {inserted} coordenadas sincronizadas!")
    print("\n📊 Resumo:")
    print(f"   • SQLite local: {len(coords)} campos")
    print(f"   • PostgreSQL Render: {inserted} campos inseridos")
    print(f"   • Campos removidos: {deleted}")
    
    print("\n✅ Agora teste a extração no Render!")
    print("   https://carrental-api-5r6g.onrender.com/admin")
    
    pg_cur.close()
    pg_conn.close()

except sqlite3.Error as e:
    print(f"\n❌ Erro no SQLite: {e}")
except psycopg2.Error as e:
    print(f"\n❌ Erro no PostgreSQL: {e}")
    print(f"   Detalhes: {e.pgerror}")
except Exception as e:
    print(f"\n❌ Erro: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*60)
