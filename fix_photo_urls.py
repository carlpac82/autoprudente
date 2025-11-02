#!/usr/bin/env python3
"""
Corrige URLs de fotos que estão com loading-car.png
Substitui por URLs reais do mapeamento manual
"""

import sqlite3
import re
from pathlib import Path

# Importar mapeamentos do generate_missing_mappings.py
from generate_missing_mappings import KNOWN_CODES

# Converter KNOWN_CODES para URLs completas
IMAGE_MAPPINGS_EXTENDED = {}
for model_key, code in KNOWN_CODES.items():
    IMAGE_MAPPINGS_EXTENDED[model_key] = f'https://www.carjet.com/cdn/img/cars/M/car_{code}.jpg'

# Mapeamento manual de URLs de fotos (original)
IMAGE_MAPPINGS = {
    # MINI / B1 / B2
    'fiat 500 cabrio': 'https://www.carjet.com/cdn/img/cars/M/car_L154.jpg',
    'fiat 500': 'https://www.carjet.com/cdn/img/cars/M/car_C25.jpg',
    'fiat 500x': 'https://www.carjet.com/cdn/img/cars/M/car_A112.jpg',
    'fiat panda': 'https://www.carjet.com/cdn/img/cars/M/car_C30.jpg',
    'citroen c1': 'https://www.carjet.com/cdn/img/cars/M/car_C96.jpg',
    'toyota aygo': 'https://www.carjet.com/cdn/img/cars/M/car_C29.jpg',
    'toyota aygo x': 'https://www.carjet.com/cdn/img/cars/M/car_F408.jpg',
    'volkswagen up': 'https://www.carjet.com/cdn/img/cars/M/car_C66.jpg',
    'vw up': 'https://www.carjet.com/cdn/img/cars/M/car_C66.jpg',
    'peugeot 108': 'https://www.carjet.com/cdn/img/cars/M/car_C15.jpg',
    'peugeot 108 cabrio': 'https://www.carjet.com/cdn/img/cars/M/car_L41.jpg',
    'hyundai i10': 'https://www.carjet.com/cdn/img/cars/M/car_C32.jpg',
    'kia picanto': 'https://www.carjet.com/cdn/img/cars/M/car_C59.jpg',
    'nissan micra': 'https://www.carjet.com/cdn/img/cars/M/car_C13.jpg',
    'dacia sandero': 'https://www.carjet.com/cdn/img/cars/M/car_C75.jpg',
    'skoda scala': 'https://www.carjet.com/cdn/img/cars/M/car_C166.jpg',
    
    # ECONOMY / D / E2
    'renault clio': 'https://www.carjet.com/cdn/img/cars/M/car_C04.jpg',
    'peugeot 208': 'https://www.carjet.com/cdn/img/cars/M/car_C60.jpg',
    'ford fiesta': 'https://www.carjet.com/cdn/img/cars/M/car_C17.jpg',
    'volkswagen polo': 'https://www.carjet.com/cdn/img/cars/M/car_C27.jpg',
    'vw polo': 'https://www.carjet.com/cdn/img/cars/M/car_C27.jpg',
    'hyundai i20': 'https://www.carjet.com/cdn/img/cars/M/car_C52.jpg',
    'seat ibiza': 'https://www.carjet.com/cdn/img/cars/M/car_C01.jpg',
    'citroen c3': 'https://www.carjet.com/cdn/img/cars/M/car_C06.jpg',
    'opel corsa': 'https://www.carjet.com/cdn/img/cars/M/car_A03.jpg',
    'toyota yaris': 'https://www.carjet.com/cdn/img/cars/M/car_C64.jpg',
    
    # COMPACT / F
    'volkswagen golf': 'https://www.carjet.com/cdn/img/cars/M/car_F12.jpg',
    'vw golf': 'https://www.carjet.com/cdn/img/cars/M/car_F12.jpg',
    'ford focus': 'https://www.carjet.com/cdn/img/cars/M/car_F02.jpg',
    'renault megane': 'https://www.carjet.com/cdn/img/cars/M/car_F05.jpg',
    'peugeot 308': 'https://www.carjet.com/cdn/img/cars/M/car_F22.jpg',
    'seat leon': 'https://www.carjet.com/cdn/img/cars/M/car_F39.jpg',
    
    # SUV / F / L1
    'nissan juke': 'https://www.carjet.com/cdn/img/cars/M/car_F29.jpg',
    'peugeot 2008': 'https://www.carjet.com/cdn/img/cars/M/car_F91.jpg',
    'peugeot 3008': 'https://www.carjet.com/cdn/img/cars/M/car_A132.jpg',
    'renault captur': 'https://www.carjet.com/cdn/img/cars/M/car_F44.jpg',
    'volkswagen t-cross': 'https://www.carjet.com/cdn/img/cars/M/car_F252.jpg',
    'vw t-cross': 'https://www.carjet.com/cdn/img/cars/M/car_F252.jpg',
    'citroen c3 aircross': 'https://www.carjet.com/cdn/img/cars/M/car_A782.jpg',
    'citroen c5 aircross': 'https://www.carjet.com/cdn/img/cars/M/car_A640.jpg',
    'toyota chr': 'https://www.carjet.com/cdn/img/cars/M/car_A301.jpg',
    'nissan qashqai': 'https://www.carjet.com/cdn/img/cars/M/car_F24.jpg',
    
    # PREMIUM / G
    'mini countryman': 'https://www.carjet.com/cdn/img/cars/M/car_F209.jpg',
    'mini cooper cabrio': 'https://www.carjet.com/cdn/img/cars/M/car_L118.jpg',
    
    # STATION WAGON / J2 / L2
    'peugeot 308 sw': 'https://www.carjet.com/cdn/img/cars/M/car_S06.jpg',
    'toyota corolla sw': 'https://www.carjet.com/cdn/img/cars/M/car_A590.jpg',
    'seat leon sw': 'https://www.carjet.com/cdn/img/cars/M/car_F46.jpg',
    
    # 7 SEATER / M1 / M2
    'dacia lodgy': 'https://www.carjet.com/cdn/img/cars/M/car_M117.jpg',
    'dacia jogger': 'https://www.carjet.com/cdn/img/cars/M/car_M162.jpg',
    'peugeot rifter': 'https://www.carjet.com/cdn/img/cars/M/car_M124.jpg',
    'vw caddy': 'https://www.carjet.com/cdn/img/cars/M/car_A295.jpg',
    
    # 9 SEATER / N
    'ford tourneo': 'https://www.carjet.com/cdn/img/cars/M/car_M44.jpg',
    'mercedes vito': 'https://www.carjet.com/cdn/img/cars/M/car_A230.jpg',
    'vw transporter': 'https://www.carjet.com/cdn/img/cars/M/car_M08.jpg',
}

def normalize_key(key):
    """Normaliza chave para matching"""
    k = key.lower().strip()
    # Remover sufixos
    k = re.sub(r',\s*(hybrid|electric)$', '', k)
    k = re.sub(r'\s+auto$', '', k)
    k = re.sub(r'\s+', ' ', k).strip()
    return k

def main():
    car_images_db = Path(__file__).parent / "car_images.db"
    
    if not car_images_db.exists():
        print(f"❌ Base de dados não encontrada: {car_images_db}")
        return
    
    conn = sqlite3.connect(str(car_images_db))
    cursor = conn.cursor()
    
    # Encontrar registos com loading-car.png
    cursor.execute("""
        SELECT model_key, photo_url 
        FROM car_images 
        WHERE photo_url LIKE '%loading-car.png%'
    """)
    
    loading_cars = cursor.fetchall()
    print(f"🔍 Encontrados {len(loading_cars)} registos com loading-car.png\n")
    
    fixed = 0
    not_found = []
    
    for model_key, old_url in loading_cars:
        # Normalizar chave
        normalized = normalize_key(model_key)
        
        # Procurar no mapeamento
        new_url = None
        
        # Combinar ambos os mapeamentos
        all_mappings = {**IMAGE_MAPPINGS, **IMAGE_MAPPINGS_EXTENDED}
        
        # Tentar match exato
        if normalized in all_mappings:
            new_url = all_mappings[normalized]
        else:
            # Tentar match parcial
            for map_key, map_url in all_mappings.items():
                if map_key in normalized or normalized in map_key:
                    new_url = map_url
                    break
        
        if new_url:
            cursor.execute("""
                UPDATE car_images 
                SET photo_url = ?, updated_at = datetime('now')
                WHERE model_key = ?
            """, (new_url, model_key))
            print(f"✅ {model_key}")
            print(f"   {old_url[:60]}...")
            print(f"   → {new_url}")
            print()
            fixed += 1
        else:
            not_found.append(model_key)
    
    conn.commit()
    conn.close()
    
    print("="*60)
    print(f"✅ Corrigidos: {fixed}")
    print(f"⚠️  Não encontrados: {len(not_found)}")
    
    if not_found:
        print("\n📋 Modelos sem mapeamento:")
        for model in not_found[:20]:  # Mostrar apenas os primeiros 20
            print(f"  • {model}")
        if len(not_found) > 20:
            print(f"  ... e mais {len(not_found) - 20}")
    
    print("="*60)

if __name__ == "__main__":
    main()
