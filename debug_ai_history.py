#!/usr/bin/env python3
"""
Script de diagnóstico para verificar automated_search_history
"""
import os
import json
from database import get_db_connection

def check_automated_search_history():
    """Verificar estado da tabela automated_search_history"""
    
    try:
        conn = get_db_connection()
        is_postgres = conn.__class__.__module__ == 'psycopg2.extensions'
        
        print(f"🔍 Tipo de BD: {'PostgreSQL' if is_postgres else 'SQLite'}")
        print()
        
        # 1. Verificar se tabela existe
        if is_postgres:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT EXISTS (
                        SELECT FROM information_schema.tables 
                        WHERE table_name = 'automated_search_history'
                    )
                """)
                table_exists = cur.fetchone()[0]
        else:
            cursor = conn.execute("""
                SELECT name FROM sqlite_master 
                WHERE type='table' AND name='automated_search_history'
            """)
            table_exists = cursor.fetchone() is not None
        
        if not table_exists:
            print("❌ Tabela 'automated_search_history' NÃO EXISTE!")
            return
        
        print("✅ Tabela 'automated_search_history' existe")
        print()
        
        # 2. Contar registros totais
        if is_postgres:
            with conn.cursor() as cur:
                cur.execute("SELECT COUNT(*) FROM automated_search_history")
                total = cur.fetchone()[0]
        else:
            cursor = conn.execute("SELECT COUNT(*) FROM automated_search_history")
            total = cursor.fetchone()[0]
        
        print(f"📊 Total de registros: {total}")
        
        if total == 0:
            print("⚠️  Tabela vazia - sem dados históricos")
            return
        
        # 3. Contar registros com supplier_data
        if is_postgres:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT COUNT(*) FROM automated_search_history 
                    WHERE supplier_data IS NOT NULL
                """)
                with_supplier = cur.fetchone()[0]
        else:
            cursor = conn.execute("""
                SELECT COUNT(*) FROM automated_search_history 
                WHERE supplier_data IS NOT NULL
            """)
            with_supplier = cursor.fetchone()[0]
        
        print(f"📊 Registros com supplier_data: {with_supplier}")
        
        if with_supplier == 0:
            print("❌ Nenhum registro tem supplier_data!")
            print("   A AI precisa de supplier_data para funcionar")
            return
        
        print()
        
        # 4. Mostrar amostra de dados
        print("🔍 Amostra de dados (últimos 3 registros):")
        print()
        
        if is_postgres:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT location, month_key, prices_data, supplier_data, search_date
                    FROM automated_search_history 
                    WHERE supplier_data IS NOT NULL
                    ORDER BY search_date DESC
                    LIMIT 3
                """)
                samples = cur.fetchall()
        else:
            cursor = conn.execute("""
                SELECT location, month_key, prices_data, supplier_data, search_date
                FROM automated_search_history 
                WHERE supplier_data IS NOT NULL
                ORDER BY search_date DESC
                LIMIT 3
            """)
            samples = cursor.fetchall()
        
        for idx, row in enumerate(samples, 1):
            location = row[0]
            month_key = row[1]
            prices_data = row[2]
            supplier_data = row[3]
            search_date = row[4]
            
            print(f"--- Registro {idx} ---")
            print(f"Location: {location}")
            print(f"Month: {month_key}")
            print(f"Date: {search_date}")
            
            # Parse supplier_data
            try:
                if isinstance(supplier_data, str):
                    supp = json.loads(supplier_data)
                else:
                    supp = supplier_data
                
                print(f"Grupos: {list(supp.keys())}")
                
                # Mostrar exemplo de um grupo
                if supp:
                    first_group = list(supp.keys())[0]
                    days_in_group = list(supp[first_group].keys())
                    print(f"  Exemplo - {first_group}: dias {days_in_group[:3]}")
                    
            except Exception as e:
                print(f"⚠️  Erro ao parsear supplier_data: {e}")
            
            print()
        
        print("✅ Diagnóstico concluído")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Erro no diagnóstico: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_automated_search_history()
