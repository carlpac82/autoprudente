#!/usr/bin/env python3
"""
Script para corrigir numeração do DR no PostgreSQL (Render)
Última numeração usada: DR39/2025
Próxima: DR40/2025
"""

import os
import psycopg2
from datetime import datetime

# URL do PostgreSQL do Render (da variável de ambiente)
DATABASE_URL = os.getenv('DATABASE_URL')

if not DATABASE_URL:
    print("❌ DATABASE_URL não encontrada!")
    print("💡 Execute no Render Shell ou defina DATABASE_URL localmente")
    exit(1)

try:
    print("🔄 Conectando ao PostgreSQL...")
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    
    # Verificar estado atual
    print("\n📊 Estado atual:")
    cur.execute("SELECT id, current_year, current_number, prefix, updated_at FROM damage_report_numbering WHERE id = 1")
    row = cur.fetchone()
    
    if row:
        print(f"   ID: {row[0]}")
        print(f"   Ano: {row[1]}")
        print(f"   Número Atual: {row[2]}")
        print(f"   Prefixo: {row[3]}")
        print(f"   Atualizado: {row[4]}")
        print(f"   Próximo DR: {row[3]}{row[2] + 1:02d}/{row[1]}")
    else:
        print("   ⚠️ Nenhum registro encontrado!")
    
    # Atualizar para 39 (próximo será 40)
    print("\n🔧 Atualizando para current_number = 39...")
    cur.execute("""
        UPDATE damage_report_numbering
        SET current_number = 39, 
            current_year = 2025, 
            prefix = 'DR',
            updated_at = %s
        WHERE id = 1
    """, (datetime.now().isoformat(),))
    
    conn.commit()
    
    # Verificar resultado
    print("\n✅ Estado após atualização:")
    cur.execute("SELECT id, current_year, current_number, prefix, updated_at FROM damage_report_numbering WHERE id = 1")
    row = cur.fetchone()
    
    if row:
        print(f"   ID: {row[0]}")
        print(f"   Ano: {row[1]}")
        print(f"   Número Atual: {row[2]}")
        print(f"   Prefixo: {row[3]}")
        print(f"   Atualizado: {row[4]}")
        print(f"   ✅ Próximo DR: {row[3]}{row[2] + 1:02d}/{row[1]}")
    
    print("\n🎉 Numeração atualizada com sucesso!")
    print("   Próximo Damage Report será: DR40/2025")
    
    cur.close()
    conn.close()

except Exception as e:
    print(f"\n❌ Erro: {e}")
    import traceback
    traceback.print_exc()
