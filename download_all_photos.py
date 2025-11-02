#!/usr/bin/env python3
"""
Download de todas as fotos dos carros
Faz download das URLs em car_images.db e guarda em data.db
"""

import sqlite3
import httpx
import asyncio
from pathlib import Path

async def download_all_photos():
    # Conectar às bases de dados
    car_images_db = Path(__file__).parent / "car_images.db"
    data_db = Path(__file__).parent / "data.db"
    
    if not car_images_db.exists():
        print(f"❌ Base de dados não encontrada: {car_images_db}")
        return
    
    # Ler URLs de car_images.db
    conn_images = sqlite3.connect(str(car_images_db))
    cursor = conn_images.cursor()
    
    cursor.execute("""
        SELECT model_key, photo_url 
        FROM car_images 
        WHERE photo_url IS NOT NULL 
        AND photo_url != ''
        AND photo_url NOT LIKE '%loading-car%'
    """)
    
    photos = cursor.fetchall()
    conn_images.close()
    
    print(f"🔍 Encontradas {len(photos)} fotos para download\n")
    
    # Conectar a data.db
    conn_data = sqlite3.connect(str(data_db))
    cursor_data = conn_data.cursor()
    
    # Criar tabela se não existir (sem updated_at para compatibilidade)
    cursor_data.execute("""
        CREATE TABLE IF NOT EXISTS vehicle_photos (
            vehicle_name TEXT PRIMARY KEY,
            photo_data BLOB,
            content_type TEXT
        )
    """)
    
    downloaded = 0
    skipped = 0
    errors = 0
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        for model_key, photo_url in photos:
            try:
                # Verificar se já existe
                existing = cursor_data.execute(
                    "SELECT vehicle_name FROM vehicle_photos WHERE vehicle_name = ?",
                    (model_key,)
                ).fetchone()
                
                if existing:
                    print(f"⏭️  {model_key} (já existe)")
                    skipped += 1
                    continue
                
                # Download da foto
                print(f"📥 Downloading {model_key}...")
                response = await client.get(photo_url)
                
                if response.status_code == 200:
                    photo_data = response.content
                    content_type = response.headers.get('content-type', 'image/jpeg')
                    
                    # Guardar na base de dados
                    cursor_data.execute("""
                        INSERT OR REPLACE INTO vehicle_photos 
                        (vehicle_name, photo_data, content_type)
                        VALUES (?, ?, ?)
                    """, (model_key, photo_data, content_type))
                    
                    conn_data.commit()
                    print(f"   ✅ {model_key} ({len(photo_data)} bytes)")
                    downloaded += 1
                else:
                    print(f"   ❌ {model_key} (HTTP {response.status_code})")
                    errors += 1
                    
            except Exception as e:
                print(f"   ❌ {model_key}: {e}")
                errors += 1
    
    conn_data.close()
    
    print("\n" + "="*60)
    print(f"✅ Downloaded: {downloaded}")
    print(f"⏭️  Skipped: {skipped}")
    print(f"❌ Errors: {errors}")
    print(f"📊 Total: {downloaded + skipped}/{len(photos)}")
    print("="*60)

if __name__ == "__main__":
    asyncio.run(download_all_photos())
