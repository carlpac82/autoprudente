#!/usr/bin/env python3
"""
Teste direto de atualização de numeração DR
Atualizar para DR 40/2025
"""

import os
import sys
from datetime import datetime

# Configurar DATABASE_URL do Render
os.environ['DATABASE_URL'] = 'postgresql://carrental_database_user:EEPUc9kD1e5RnVfXPNMqLXo6XbBdTevA@dpg-ct05cnm8ii6s73fq3jpg-a.frankfurt-postgres.render.com/carrental_database'

print("🔧 Importando módulos...")
import psycopg2

def update_numbering():
    """Atualizar numeração DR para 40"""
    try:
        db_url = os.environ['DATABASE_URL']
        print(f"📊 Conectando ao PostgreSQL...")
        
        # Adicionar SSL mode se necessário
        if '?sslmode=' not in db_url:
            db_url += '?sslmode=require'
        
        conn = psycopg2.connect(db_url)
        cur = conn.cursor()
        
        # Verificar valor atual
        print("\n📋 ANTES:")
        cur.execute("SELECT current_number, prefix, current_year FROM damage_report_numbering WHERE id = 1")
        before = cur.fetchone()
        if before:
            print(f"   current_number = {before[0]}")
            print(f"   prefix = {before[1]}")
            print(f"   current_year = {before[2]}")
        else:
            print("   ❌ Nenhum registro encontrado!")
            return
        
        # Atualizar para 40
        current_year = datetime.now().year
        new_number = 40
        prefix = 'DR'
        
        print(f"\n🔄 ATUALIZANDO para {new_number}...")
        cur.execute("""
            UPDATE damage_report_numbering
            SET current_number = %s, prefix = %s, current_year = %s, updated_at = %s
            WHERE id = 1
        """, (new_number, prefix, current_year, datetime.now().isoformat()))
        
        rows_affected = cur.rowcount
        print(f"   {rows_affected} linha(s) afetada(s)")
        
        # COMMIT
        print("\n💾 COMMIT...")
        conn.commit()
        print("   ✅ Commit executado")
        
        # Verificar se persistiu
        print("\n📋 DEPOIS:")
        cur.execute("SELECT current_number, prefix, current_year FROM damage_report_numbering WHERE id = 1")
        after = cur.fetchone()
        if after:
            print(f"   current_number = {after[0]}")
            print(f"   prefix = {after[1]}")
            print(f"   current_year = {after[2]}")
            
            if after[0] == new_number:
                print("\n✅ SUCESSO! Numeração atualizada para 40")
                print(f"   Próximo DR será: DR{(new_number+1):02d}/{current_year}")
            else:
                print(f"\n❌ ERRO! Esperado {new_number}, encontrado {after[0]}")
        
        cur.close()
        conn.close()
        
    except Exception as e:
        print(f"\n❌ ERRO: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    update_numbering()
