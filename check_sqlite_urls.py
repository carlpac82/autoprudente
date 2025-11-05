"""
Verificar se o SQLite local tem os links da Carjet
"""

import sqlite3

DB_PATH = "data.db"

try:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    print("=" * 80)
    print("🔍 VERIFICANDO SQLITE LOCAL")
    print("=" * 80)
    
    # Check vehicle_photos
    cursor.execute("""
        SELECT 
            COUNT(*) as total,
            COUNT(photo_url) as with_url
        FROM vehicle_photos
    """)
    row = cursor.fetchone()
    total, with_url = row
    
    print(f"\n📊 VEHICLE_PHOTOS:")
    print(f"  Total: {total} veículos")
    print(f"  Com photo_url: {with_url} ({with_url/total*100:.1f}%)" if total > 0 else "  Sem dados")
    
    if with_url > 0:
        print(f"\n🔗 EXEMPLOS (primeiros 5):")
        cursor.execute("""
            SELECT vehicle_name, photo_url
            FROM vehicle_photos
            WHERE photo_url IS NOT NULL
            LIMIT 5
        """)
        for vehicle, url in cursor.fetchall():
            print(f"  {vehicle}: {url}")
        
        print(f"\n✅ LINKS ENCONTRADOS NO SQLITE!")
        print(f"   Posso criar script para copiar {with_url} links para PostgreSQL")
    else:
        print(f"\n❌ SQLite também não tem links")
    
    conn.close()
    
except Exception as e:
    print(f"❌ Erro: {e}")

print("\n" + "=" * 80)
