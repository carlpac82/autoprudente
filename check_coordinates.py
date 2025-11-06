"""
Verificar coordenadas no PostgreSQL
"""

import psycopg2

DATABASE_URL = "postgresql://carrental_user:cmXcauHIuQinAyDQjcB9XiVMU0Gaxviz@dpg-d44gvnm3jp1c73dc2edg-a.frankfurt-postgres.render.com/carrental_db_9klo?sslmode=require"

pg_conn = psycopg2.connect(DATABASE_URL)
pg_cursor = pg_conn.cursor()

print("=" * 80)
print("🔍 VERIFICAR COORDENADAS DR NO POSTGRESQL")
print("=" * 80)

# Ver quantas coordenadas existem
pg_cursor.execute("""
    SELECT COUNT(*) FROM damage_report_coordinates
""")

count = pg_cursor.fetchone()[0]

print(f"\n📊 Total de coordenadas: {count}")

if count > 0:
    # Ver alguns exemplos
    pg_cursor.execute("""
        SELECT field_id, x, y, width, height, page, template_version
        FROM damage_report_coordinates
        ORDER BY field_id
        LIMIT 10
    """)
    
    print(f"\n📋 PRIMEIRAS 10 COORDENADAS:")
    for row in pg_cursor.fetchall():
        field_id, x, y, width, height, page, version = row
        print(f"  {field_id}: ({x:.1f}, {y:.1f}) - {width:.1f}x{height:.1f} [pg {page}] v{version}")
else:
    print("\n⚠️  Nenhuma coordenada encontrada!")
    print("   As coordenadas precisam ser mapeadas primeiro.")

pg_conn.close()

print("\n" + "=" * 80)
print("✅ Verificação completa!")
