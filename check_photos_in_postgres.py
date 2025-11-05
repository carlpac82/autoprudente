#!/usr/bin/env python3
"""
Verifica se as fotos estão realmente no PostgreSQL do Render
"""
import psycopg2
import sys

# Connection string do Render
DATABASE_URL = "postgresql://carrental_user:cmXcauHIuQinAyDQjcBXiVMU0Gaxviz@dpg-d44gvnm3jp1c73dc2edg-a.frankfurt-postgres.render.com/carrental_db_9klo"

try:
    print("🔍 Conectando ao PostgreSQL do Render...")
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    
    # Verificar tabelas
    print("\n📊 Verificando tabelas...")
    cursor.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public' 
        AND table_name IN ('vehicle_photos', 'vehicle_images')
        ORDER BY table_name
    """)
    tables = cursor.fetchall()
    print(f"Tabelas encontradas: {[t[0] for t in tables]}")
    
    # Contar fotos em vehicle_photos
    print("\n📸 Contando fotos em vehicle_photos...")
    cursor.execute("SELECT COUNT(*) FROM vehicle_photos WHERE photo_data IS NOT NULL")
    count_photos = cursor.fetchone()[0]
    print(f"Total de fotos em vehicle_photos: {count_photos}")
    
    # Contar fotos em vehicle_images
    print("\n🖼️  Contando fotos em vehicle_images...")
    cursor.execute("SELECT COUNT(*) FROM vehicle_images WHERE image_data IS NOT NULL")
    count_images = cursor.fetchone()[0]
    print(f"Total de fotos em vehicle_images: {count_images}")
    
    # Listar primeiras 20 fotos
    print("\n📋 Primeiras 20 fotos em vehicle_images:")
    cursor.execute("""
        SELECT vehicle_key, LENGTH(image_data) as size, content_type 
        FROM vehicle_images 
        ORDER BY vehicle_key 
        LIMIT 20
    """)
    for row in cursor.fetchall():
        print(f"  - {row[0]}: {row[1]} bytes, {row[2]}")
    
    # Verificar se existe 'audi a1'
    print("\n🔍 Procurando 'audi a1'...")
    cursor.execute("SELECT vehicle_key, LENGTH(image_data) FROM vehicle_images WHERE vehicle_key LIKE %s", ('audi a1%',))
    results = cursor.fetchall()
    if results:
        for row in results:
            print(f"  ✅ Encontrado: {row[0]} ({row[1]} bytes)")
    else:
        print("  ❌ Não encontrado")
        
    # Verificar se existe 'volkswagen golf'
    print("\n🔍 Procurando 'volkswagen golf'...")
    cursor.execute("SELECT vehicle_key, LENGTH(image_data) FROM vehicle_images WHERE vehicle_key LIKE %s", ('volkswagen golf%',))
    results = cursor.fetchall()
    if results:
        for row in results:
            print(f"  ✅ Encontrado: {row[0]} ({row[1]} bytes)")
    else:
        print("  ❌ Não encontrado")
    
    # Verificar nomes exatos que aparecem no vehicle editor
    print("\n🔍 Procurando nomes exatos do vehicle editor...")
    test_names = ['bmw x1', 'bmw 3 series sw', 'bmw 4 series gran coupe', 'bmw 5 series']
    for name in test_names:
        cursor.execute("SELECT vehicle_key, LENGTH(image_data) FROM vehicle_images WHERE vehicle_key = %s", (name,))
        result = cursor.fetchone()
        if result:
            print(f"  ✅ {name}: {result[1]} bytes")
        else:
            print(f"  ❌ {name}: não encontrado")
    
    cursor.close()
    conn.close()
    print("\n✅ Verificação completa!")
    
except Exception as e:
    print(f"\n❌ ERRO: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
