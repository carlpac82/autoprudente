#!/usr/bin/env python3
"""
Testa queries LIKE no PostgreSQL
"""
import psycopg2

DATABASE_URL = "postgresql://carrental_user:cmXcauHIuQinAyDQjcB9XiVMU0Gaxviz@dpg-d44gvnm3jp1c73dc2edg-a.frankfurt-postgres.render.com/carrental_db_9klo?sslmode=require"

try:
    print("🔍 Conectando...")
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    
    # Teste 1: Query simples
    print("\n✅ Teste 1: SELECT simples")
    cursor.execute("SELECT vehicle_key FROM vehicle_images WHERE vehicle_key = %s", ('fiat 500',))
    result = cursor.fetchone()
    print(f"   Resultado: {result}")
    
    # Teste 2: LIKE com %
    print("\n✅ Teste 2: LIKE com %")
    cursor.execute("SELECT vehicle_key FROM vehicle_images WHERE vehicle_key LIKE %s LIMIT 1", ('fiat%',))
    result = cursor.fetchone()
    print(f"   Resultado: {result}")
    
    # Teste 3: LIKE com % no meio
    print("\n✅ Teste 3: LIKE com % no meio")
    cursor.execute("SELECT vehicle_key FROM vehicle_images WHERE vehicle_key LIKE %s LIMIT 1", ('%500%',))
    result = cursor.fetchone()
    print(f"   Resultado: {result}")
    
    # Teste 4: Múltiplos parâmetros com %
    print("\n✅ Teste 4: Múltiplos parâmetros com %")
    cursor.execute("""
        SELECT vehicle_key FROM vehicle_images 
        WHERE vehicle_key LIKE %s 
        AND vehicle_key NOT LIKE %s 
        LIMIT 1
    """, ('fiat%', '%sw%'))
    result = cursor.fetchone()
    print(f"   Resultado: {result}")
    
    print("\n🎉 Todos os testes passaram!")
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"\n❌ ERRO: {e}")
    import traceback
    traceback.print_exc()
