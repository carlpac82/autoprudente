#!/usr/bin/env python3
"""
Script para corrigir numeração DR no PostgreSQL do Render
Atualiza current_number para 39 (próximo será 40)
"""

import os
import psycopg2

# DATABASE_URL do Render
DATABASE_URL = "postgresql://carrental_api_user:ioNy2e66qm4LgOAbjPy7c5pf3BHW1SdP@dpg-crsqvpr6l47c739u4uqg-a.frankfurt-postgres.render.com/carrental_api?sslmode=require"

print("🔄 Conectando ao PostgreSQL do Render...")
try:
    conn = psycopg2.connect(DATABASE_URL, connect_timeout=30)
    print("✅ Conectado!")
    
    # Verificar valor atual
    with conn.cursor() as cur:
        cur.execute("SELECT current_year, current_number, prefix FROM damage_report_numbering WHERE id = 1")
        row = cur.fetchone()
        
        if row:
            year, number, prefix = row
            print(f"📊 ANTES: {prefix} {number:02d}/{year}")
            
            # Atualizar para 39
            cur.execute("""
                UPDATE damage_report_numbering 
                SET current_number = 39, updated_at = NOW()
                WHERE id = 1
            """)
            conn.commit()
            
            # Verificar depois
            cur.execute("SELECT current_year, current_number, prefix FROM damage_report_numbering WHERE id = 1")
            row = cur.fetchone()
            year, number, prefix = row
            print(f"✅ DEPOIS: {prefix} {number:02d}/{year}")
            print(f"🎯 Próximo DR será: {prefix} {number+1:02d}/{year}")
        else:
            print("❌ Tabela damage_report_numbering não tem registos!")
    
    conn.close()
    print("✅ Conexão fechada")
    
except Exception as e:
    print(f"❌ Erro: {e}")
