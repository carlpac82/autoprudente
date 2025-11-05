#!/usr/bin/env python3
"""
Verifica se as fotos estão no PostgreSQL do Render
Usa a connection string com SSL
"""
import psycopg2
import sys

# Connection string com SSL (atualizada)
DATABASE_URL = "postgresql://carrental_user:cmXcauHIuQinAyDQjcB9XiVMU0Gaxviz@dpg-d44gvnm3jp1c73dc2edg-a.frankfurt-postgres.render.com/carrental_db_9klo?sslmode=require"

try:
    print("🔍 Conectando ao PostgreSQL do Render (com SSL)...")
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    
    # Contar fotos em vehicle_images
    print("\n🖼️  Contando fotos em vehicle_images...")
    cursor.execute("SELECT COUNT(*) FROM vehicle_images WHERE image_data IS NOT NULL")
    count_images = cursor.fetchone()[0]
    print(f"Total de fotos em vehicle_images: {count_images}")
    
    if count_images == 0:
        print("\n❌ PROBLEMA: Nenhuma foto encontrada em vehicle_images!")
        print("As fotos NÃO foram enviadas para o PostgreSQL ou foram apagadas.")
    else:
        print(f"\n✅ {count_images} fotos encontradas!")
        
        # Listar primeiras 10
        print("\n📋 Primeiras 10 fotos:")
        cursor.execute("""
            SELECT vehicle_key, LENGTH(image_data) as size, content_type 
            FROM vehicle_images 
            ORDER BY vehicle_key 
            LIMIT 10
        """)
        for row in cursor.fetchall():
            print(f"  - {row[0]}: {row[1]} bytes, {row[2]}")
        
        # Procurar carros específicos
        test_cars = ['audi a1', 'bmw x1', 'volkswagen golf', 'fiat 500']
        print("\n🔍 Procurando carros específicos:")
        for car in test_cars:
            cursor.execute("SELECT vehicle_key, LENGTH(image_data) FROM vehicle_images WHERE LOWER(vehicle_key) = %s", (car.lower(),))
            result = cursor.fetchone()
            if result:
                print(f"  ✅ {car}: {result[1]} bytes")
            else:
                # Tentar LIKE
                cursor.execute("SELECT vehicle_key, LENGTH(image_data) FROM vehicle_images WHERE LOWER(vehicle_key) LIKE %s LIMIT 1", (car.lower() + '%',))
                result = cursor.fetchone()
                if result:
                    print(f"  ⚠️  {car}: não encontrado exato, mas existe '{result[0]}' ({result[1]} bytes)")
                else:
                    print(f"  ❌ {car}: não encontrado")
    
    cursor.close()
    conn.close()
    print("\n✅ Verificação completa!")
    
except Exception as e:
    print(f"\n❌ ERRO: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
