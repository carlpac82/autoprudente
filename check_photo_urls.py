"""
Verificar quantas fotos de veículos têm URLs da Carjet
"""

import psycopg2

DATABASE_URL = "postgresql://carrental_user:cmXcauHIuQinAyDQjcB9XiVMU0Gaxviz@dpg-d44gvnm3jp1c73dc2edg-a.frankfurt-postgres.render.com/carrental_db_9klo?sslmode=require"

pg_conn = psycopg2.connect(DATABASE_URL)
pg_cursor = pg_conn.cursor()

print("=" * 80)
print("🔍 VERIFICANDO LINKS DE FOTOS DA CARJET")
print("=" * 80)

# 1. vehicle_photos
print("\n📊 VEHICLE_PHOTOS:")
pg_cursor.execute("""
    SELECT 
        COUNT(*) as total,
        COUNT(photo_url) as with_url,
        COUNT(photo_data) as with_data
    FROM vehicle_photos
""")
row = pg_cursor.fetchone()
if row:
    total, with_url, with_data = row
    print(f"  Total: {total} veículos")
    print(f"  Com photo_url: {with_url} ({with_url/total*100:.1f}%)" if total > 0 else "  Sem dados")
    print(f"  Com photo_data: {with_data} ({with_data/total*100:.1f}%)" if total > 0 else "  Sem dados")

# 2. vehicle_images
print("\n📊 VEHICLE_IMAGES:")
try:
    pg_cursor.execute("""
        SELECT 
            COUNT(*) as total,
            COUNT(source_url) as with_url,
            COUNT(image_data) as with_data
        FROM vehicle_images
    """)
    row = pg_cursor.fetchone()
    if row:
        total, with_url, with_data = row
        print(f"  Total: {total} veículos")
        print(f"  Com source_url: {with_url} ({with_url/total*100:.1f}%)" if total > 0 else "  Sem dados")
        print(f"  Com image_data: {with_data} ({with_data/total*100:.1f}%)" if total > 0 else "  Sem dados")
except Exception as e:
    print(f"  ❌ Erro: {e}")

# 3. Exemplos de URLs
print("\n🔗 EXEMPLOS DE URLs (primeiros 5):")
pg_cursor.execute("""
    SELECT vehicle_name, photo_url
    FROM vehicle_photos
    WHERE photo_url IS NOT NULL
    LIMIT 5
""")
for row in pg_cursor.fetchall():
    vehicle, url = row
    print(f"  {vehicle}: {url}")

pg_conn.close()

print("\n" + "=" * 80)
print("✅ Verificação completa!")
