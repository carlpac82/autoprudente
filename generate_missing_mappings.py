#!/usr/bin/env python3
"""
Gera mapeamentos de fotos para modelos que ainda têm loading-car.png
Tenta inferir o código CarJet baseado no nome do modelo
"""

import sqlite3
import re
from pathlib import Path

# Mapeamento de modelos para códigos CarJet conhecidos
KNOWN_CODES = {
    # Baseado nos códigos que já funcionam
    'citroen c4': 'A17',
    'citroen c4 cactus': 'C51',
    'seat arona': 'F194',
    'opel adam': 'C50',
    'kia sportage': 'F43',
    'ford ka': 'N07',
    'volkswagen t-roc': 'F252',  # Similar ao T-Cross
    'vw t-roc': 'F252',
    'ford kuga': 'F41',
    'vw taigo': 'F352',
    'volkswagen taigo': 'F352',
    'opel astra': 'F73',
    'kia ceed': 'C21',
    'audi a1': 'C42',
    'ford ecosport': 'A606',
    'opel crossland x': 'A444',
    'renault twingo': 'C61',
    'opel mokka': 'A444',  # Similar ao Crossland
    'hyundai i30': 'C41',
    'skoda octavia': 'I12',
    'skoda fabia sw': 'S34',
    'skoda kamiq': 'F310',
    'skoda karoq': 'A822',
    'skoda kodiaq': 'A822',  # Similar ao Karoq
    'hyundai tucson': 'F310',
    'hyundai kauai': 'F44',  # Similar ao Captur
    'hyundai kona': 'F191',
    'kia stonic': 'F119',
    'jeep avenger': 'L164',
    'jeep renegade': 'A222',
    'mitsubishi asx': 'F178',
    'mitsubishi spacestar': 'C190',
    'mazda cx3': 'F179',
    'mazda 2': 'C64',  # Similar ao Yaris
    'seat alhambra': 'M56',  # Similar ao Sharan
    'seat ateca': 'F154',
    'seat mii': 'C66',  # Similar ao UP
    'fiat tipo': 'F72',
    'fiat tipo sw': 'F72',
    'fiat talento': 'M49',
    'fiat 500l': 'C43',
    'fiat 600': 'C25',  # Similar ao 500
    'ford galaxy': 'M03',
    'ford transit': 'M02',
    'ford transit custom': 'M02',
    'ford puma': 'A999',
    'toyota hilux': 'F326',
    'toyota rav4': 'A1000',
    'toyota proace': 'M136',
    'toyota bz4x': 'A301',  # Similar ao C-HR
    'renault austral': 'F430',
    'renault arkana': 'A1159',
    'renault trafic': 'A581',
    'renault grand scenic': 'M15',
    'peugeot 5008': 'M27',
    'peugeot 508': 'F65',
    'peugeot traveller': 'M86',
    'peugeot e-208': 'C60',  # Mesmo que 208
    'peugeot e-traveller': 'M86',  # Mesmo que Traveller
    'citroen spacetourer': 'A261',
    'citroen grand picasso': 'A219',
    'citroen c4 picasso': 'A522',
    'citroen c4 grand spacetourer': 'A1430',
    'citroen c4 x': 'A17',  # Similar ao C4
    'citroen elysee': 'C06',  # Similar ao C3
    'dacia duster': 'F44',  # Similar ao Captur
    'vw sharan': 'M56',
    'vw multivan': 'A406',
    'vw caravelle': 'M63',
    'vw passat': 'I11',
    'vw arteon sw': 'I11',  # Similar ao Passat
    'vw beetle cabrio': 'L44',
    'volkswagen eos cabrio': 'L44',  # Similar ao Beetle
    'volkswagen id.3': 'C25',  # Placeholder elétrico
    'volkswagen id.5': 'A112',  # Placeholder elétrico
    'cupra born': 'C25',  # Baseado no 500
    'cupra formentor': 'A1185',
    'cupra leon sw': 'A1426',
    'ds4': 'A1637',
    'ds7': 'A1637',
    'tesla model 3': 'C25',  # Placeholder
    'volvo ex30': 'F252',  # Placeholder
    'volvo v60': 'I11',  # Similar a station wagons
    'volvo xc40': 'F252',
    'volvo xc60': 'A830',
    'volvo xc90': 'A830',
    'bmw 1 series': 'F12',  # Similar ao Golf
    'bmw 2 series': 'F12',
    'bmw 3 series': 'I11',
    'bmw 4 series': 'I11',
    'bmw 5 series': 'I11',
    'bmw x1': 'F252',
    'bmw x5': 'A830',
    'mercedes a class': 'F12',
    'mercedes b class': 'F12',
    'mercedes c class': 'I11',
    'mercedes e class': 'I11',
    'mercedes s class': 'I11',
    'mercedes cla': 'I11',
    'mercedes cle': 'I11',
    'mercedes gla': 'F252',
    'mercedes glb': 'GZ399',
    'mercedes glc': 'A830',
    'mercedes gle': 'A830',
    'mercedes v class': 'A1336',
    'mercedes eqa': 'F252',  # Elétrico similar ao GLA
    'mercedes eqb': 'GZ399',  # Elétrico similar ao GLB
    'mercedes eqc': 'A830',  # Elétrico similar ao GLC
    'mini one cabrio': 'L118',
    'alfa romeo giulietta': 'F39',  # Similar ao Leon
    'audi a3': 'F12',
    'audi a5': 'I11',
    'audi q2': 'F252',
    'audi q4': 'A830',
    'range rover evoque': 'A830',
    'porsche cayenne': 'A830',
    'mg zs': 'F252',
    'mg ehs': 'A830',
    'byd seal u': 'A830',
    'kia niro': 'F252',
    'mazda mx5': 'L118',
    
    # ÚLTIMOS 7 MODELOS (100% cobertura!)
    'vw tiguan': 'A110',
    'opel zafira': 'M05',
    'mercedes benz vito': 'A230',
    'opel vivaro': 'M34',
    'opel grandland x': 'A304',
    'renault scenic': 'A571',
    'mitsubishi eclipse cross': 'F178',
}

def normalize_key(key):
    """Normaliza chave para matching"""
    k = key.lower().strip()
    # Remover sufixos
    k = re.sub(r',\s*(hybrid|electric)$', '', k)
    k = re.sub(r'\s+auto$', '', k)
    k = re.sub(r'\s+(cabrio|sw|4x4|sedan|5 door|7 seater)$', '', k)
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
        ORDER BY model_key
    """)
    
    loading_cars = cursor.fetchall()
    print(f"🔍 Encontrados {len(loading_cars)} modelos com loading-car.png\n")
    print("="*80)
    print("CÓDIGO PYTHON PARA ADICIONAR AO main.py:\n")
    print("# Adicionar ao IMAGE_MAPPINGS (linha ~9676):")
    print()
    
    generated = 0
    
    for model_key, old_url in loading_cars:
        normalized = normalize_key(model_key)
        
        if normalized in KNOWN_CODES:
            code = KNOWN_CODES[normalized]
            url = f"https://www.carjet.com/cdn/img/cars/M/car_{code}.jpg"
            print(f"    '{model_key}': '{url}',")
            generated += 1
    
    print()
    print("="*80)
    print(f"✅ Gerados {generated} mapeamentos")
    print()
    print("📋 INSTRUÇÕES:")
    print("1. Copiar o código acima")
    print("2. Adicionar ao dicionário IMAGE_MAPPINGS em main.py (linha ~9676)")
    print("3. Executar: python3 fix_photo_urls.py")
    print("4. Verificar: python3 diagnose_photos.py")
    
    conn.close()

if __name__ == "__main__":
    main()
