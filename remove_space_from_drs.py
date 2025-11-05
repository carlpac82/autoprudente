"""
Remover espaço dos dr_numbers no PostgreSQL
DR 01/2025 → DR01/2025
"""

import psycopg2

DATABASE_URL = "postgresql://carrental_user:cmXcauHIuQinAyDQjcB9XiVMU0Gaxviz@dpg-d44gvnm3jp1c73dc2edg-a.frankfurt-postgres.render.com/carrental_db_9klo?sslmode=require"

pg_conn = psycopg2.connect(DATABASE_URL)
pg_cursor = pg_conn.cursor()

print("🔧 Removendo espaços dos dr_numbers...")
print("=" * 60)

# Buscar todos os DRs
pg_cursor.execute("SELECT dr_number FROM damage_reports ORDER BY dr_number")
rows = pg_cursor.fetchall()

updated = 0
errors = []

for row in rows:
    old_dr = row[0]
    
    # Remover espaço: "DR 01/2025" → "DR01/2025"
    if ' ' in old_dr:
        new_dr = old_dr.replace(' ', '')
        
        try:
            pg_cursor.execute("""
                UPDATE damage_reports
                SET dr_number = %s
                WHERE dr_number = %s
            """, (new_dr, old_dr))
            
            pg_conn.commit()
            print(f"✅ {old_dr} → {new_dr}")
            updated += 1
            
        except Exception as e:
            errors.append(f"{old_dr}: {str(e)}")
            print(f"❌ {old_dr} - ERRO: {e}")
            pg_conn.rollback()
    else:
        print(f"⏭️  {old_dr} - Já sem espaço")

print("=" * 60)
print(f"✅ Atualizados: {updated}")
print(f"❌ Erros: {len(errors)}")

if errors:
    print("\nERROS:")
    for error in errors:
        print(f"  - {error}")

pg_conn.close()
print("\n✅ Concluído!")
