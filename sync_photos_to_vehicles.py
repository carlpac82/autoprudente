#!/usr/bin/env python3
"""
Sincroniza fotos de car_images.db para vehicle_images em data.db
Faz matching inteligente entre os nomes dos carros
"""

import sqlite3
import re
from pathlib import Path

def normalize_name(name):
    """Normaliza nome do carro para matching"""
    name = name.lower().strip()
    
    # Substituir volkswagen por vw
    name = name.replace('volkswagen', 'vw')
    
    # Remover hífens de modelos (c-hr → chr, cx-3 → cx3)
    name = re.sub(r'([a-z])[-]([a-z0-9])', r'\1\2', name)
    
    # Remover "c4" de "c4 grand picasso" → "grand picasso"
    name = re.sub(r'^citroen c4 grand picasso', 'citroen grand picasso', name)
    
    # Remover sufixos comuns (múltiplas passagens)
    name = re.sub(r'\s+(ou\s*similar|or\s*similar).*$', '', name, flags=re.IGNORECASE)
    name = re.sub(r',\s*(hybrid|electric|diesel|automatic)$', '', name)
    
    # Remover sufixos de variantes (repetir para pegar todos)
    for _ in range(3):  # Repetir 3 vezes para pegar múltiplos sufixos
        name = re.sub(r'\s+(auto|automatic|automático|hybrid|electric|diesel|4x4|cabrio|sw|sedan|5 door|7 seater|4p|5p)$', '', name)
        name = re.sub(r',\s*(hybrid|electric|diesel|automatic)$', '', name)
    
    # Normalizar espaços
    name = re.sub(r'\s+', ' ', name).strip()
    
    # Remover "ds " e deixar só número (ds 4 → ds4)
    name = re.sub(r'^ds\s+(\d)', r'ds\1', name)
    
    return name

def main():
    base_path = Path(__file__).parent
    car_images_db = base_path / "car_images.db"
    data_db = base_path / "data.db"
    
    if not car_images_db.exists():
        print(f"❌ {car_images_db} não encontrado")
        return
    
    if not data_db.exists():
        print(f"❌ {data_db} não encontrado")
        return
    
    # Ler fotos de car_images.db
    print("📥 Lendo fotos de car_images.db...")
    conn_images = sqlite3.connect(str(car_images_db))
    photos = {}
    
    cursor = conn_images.cursor()
    rows = cursor.execute("""
        SELECT model_key, photo_url 
        FROM car_images 
        WHERE photo_url IS NOT NULL 
        AND photo_url != ''
        AND photo_url NOT LIKE '%loading-car%'
    """).fetchall()
    
    for model_key, photo_url in rows:
        normalized = normalize_name(model_key)
        photos[normalized] = (model_key, photo_url)
    
    conn_images.close()
    print(f"✅ Encontradas {len(photos)} fotos únicas")
    
    # Ler veículos de data.db (via carjet_direct.py)
    print("\n📥 Lendo veículos de VEHICLES...")
    try:
        from carjet_direct import VEHICLES
        vehicle_names = list(VEHICLES.keys())
        print(f"✅ Encontrados {len(vehicle_names)} veículos")
    except Exception as e:
        print(f"❌ Erro ao importar VEHICLES: {e}")
        return
    
    # Fazer matching
    print("\n🔗 Fazendo matching entre veículos e fotos...")
    conn_data = sqlite3.connect(str(data_db))
    cursor_data = conn_data.cursor()
    
    matched = 0
    not_matched = 0
    
    for vehicle_name in vehicle_names:
        normalized = normalize_name(vehicle_name)
        
        if normalized in photos:
            original_key, photo_url = photos[normalized]
            
            # Verificar se já existe foto
            existing = cursor_data.execute(
                "SELECT vehicle_key FROM vehicle_images WHERE vehicle_key = ?",
                (vehicle_name,)
            ).fetchone()
            
            if existing:
                print(f"⏭️  {vehicle_name} (já tem foto)")
            else:
                # Baixar foto e guardar
                print(f"📥 {vehicle_name} ← {original_key}")
                
                import httpx
                try:
                    response = httpx.get(photo_url, timeout=10.0)
                    if response.status_code == 200:
                        image_data = response.content
                        content_type = response.headers.get('content-type', 'image/jpeg')
                        
                        cursor_data.execute("""
                            INSERT OR REPLACE INTO vehicle_images 
                            (vehicle_key, image_data, content_type, source_url)
                            VALUES (?, ?, ?, ?)
                        """, (vehicle_name, image_data, content_type, photo_url))
                        
                        conn_data.commit()
                        print(f"   ✅ {len(image_data)} bytes")
                        matched += 1
                    else:
                        print(f"   ❌ HTTP {response.status_code}")
                        not_matched += 1
                except Exception as e:
                    print(f"   ❌ Erro: {e}")
                    not_matched += 1
        else:
            print(f"❌ {vehicle_name} (sem foto correspondente)")
            not_matched += 1
    
    conn_data.close()
    
    print("\n" + "="*60)
    print(f"✅ Matched e baixados: {matched}")
    print(f"⏭️  Já existiam: {len(vehicle_names) - matched - not_matched}")
    print(f"❌ Não encontrados: {not_matched}")
    print(f"📊 Total de veículos: {len(vehicle_names)}")
    print("="*60)
    
    # Verificar total final
    conn_data = sqlite3.connect(str(data_db))
    total = conn_data.execute("SELECT COUNT(*) FROM vehicle_images").fetchone()[0]
    conn_data.close()
    
    print(f"\n📊 Total de fotos em vehicle_images: {total}")

if __name__ == "__main__":
    main()
