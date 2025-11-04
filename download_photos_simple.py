#!/usr/bin/env python3
"""
Script simples para baixar fotos do CarJet
Usa a lista de carros já existente na base de dados
"""

import sqlite3
import httpx
import asyncio
from datetime import datetime
from pathlib import Path

# Lista de URLs de fotos conhecidas do CarJet
# Formato: https://www.carjet.com/cdn/img/cars/M/car_C{número}.jpg
PHOTO_URLS = {
    'opel corsa': 'https://www.carjet.com/cdn/img/cars/M/car_C82.jpg',
    'renault clio': 'https://www.carjet.com/cdn/img/cars/M/car_C04.jpg',
    'fiat panda': 'https://www.carjet.com/cdn/img/cars/M/car_C45.jpg',
    'vw polo': 'https://www.carjet.com/cdn/img/cars/M/car_C27.jpg',
    'volkswagen polo': 'https://www.carjet.com/cdn/img/cars/M/car_C27.jpg',
    'toyota aygo': 'https://www.carjet.com/cdn/img/cars/M/car_C29.jpg',
    'volkswagen up': 'https://www.carjet.com/cdn/img/cars/M/car_C66.jpg',
    'opel corsa auto': 'https://www.carjet.com/cdn/img/cars/M/car_A03.jpg',
    # Adicionar mais conforme necessário
}

async def download_photos():
    """Baixa fotos para os carros na base de dados"""
    
    db_path = Path(__file__).parent / "data.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Buscar todos os nomes de carros únicos
    cursor.execute("""
        SELECT DISTINCT edited_name 
        FROM vehicle_name_overrides
        WHERE edited_name IS NOT NULL AND edited_name != ''
        ORDER BY edited_name
    """)
    
    vehicles = [row[0] for row in cursor.fetchall()]
    
    print(f"📊 Total de veículos: {len(vehicles)}")
    print("="*60)
    
    downloaded = 0
    skipped = 0
    failed = 0
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        for idx, vehicle_name in enumerate(vehicles, 1):
            vehicle_clean = vehicle_name.lower().strip()
            
            # Verificar se já tem foto
            cursor.execute("""
                SELECT COUNT(*) FROM vehicle_photos 
                WHERE vehicle_name = ?
            """, (vehicle_clean,))
            
            has_photo = cursor.fetchone()[0] > 0
            
            if has_photo:
                print(f"[{idx}/{len(vehicles)}] ⏭️  {vehicle_name} - Já tem foto")
                skipped += 1
                continue
            
            # Procurar URL da foto
            photo_url = PHOTO_URLS.get(vehicle_clean)
            
            if not photo_url:
                print(f"[{idx}/{len(vehicles)}] ❌ {vehicle_name} - URL não encontrada")
                failed += 1
                continue
            
            # Baixar foto
            try:
                print(f"[{idx}/{len(vehicles)}] 📥 {vehicle_name}")
                print(f"                    {photo_url}")
                
                response = await client.get(photo_url)
                
                if response.status_code == 200:
                    photo_data = response.content
                    
                    # Salvar na base de dados
                    cursor.execute("""
                        INSERT OR REPLACE INTO vehicle_photos 
                        (vehicle_name, photo_data, photo_url, updated_at)
                        VALUES (?, ?, ?, ?)
                    """, (vehicle_clean, photo_data, photo_url, datetime.now().isoformat()))
                    
                    cursor.execute("""
                        INSERT OR REPLACE INTO vehicle_images 
                        (vehicle_name, image_data, image_url, updated_at)
                        VALUES (?, ?, ?, ?)
                    """, (vehicle_clean, photo_data, photo_url, datetime.now().isoformat()))
                    
                    conn.commit()
                    downloaded += 1
                    print(f"                    ✅ {len(photo_data)} bytes")
                else:
                    print(f"                    ❌ HTTP {response.status_code}")
                    failed += 1
                    
            except Exception as e:
                print(f"                    ❌ Erro: {e}")
                failed += 1
    
    conn.close()
    
    print("="*60)
    print(f"✅ Baixadas: {downloaded}")
    print(f"⏭️  Ignoradas: {skipped}")
    print(f"❌ Falharam: {failed}")
    print(f"📊 Total: {downloaded + skipped}/{len(vehicles)}")

if __name__ == "__main__":
    asyncio.run(download_photos())
