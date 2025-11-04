#!/usr/bin/env python3
"""
Download APENAS das fotos REAIS extraídas do HTML
Muito mais rápido e eficiente!
"""

import json
import requests
import os
import time
import re

def download_photo(car_data, output_dir='carjet_photos_real'):
    """Download de uma foto"""
    os.makedirs(output_dir, exist_ok=True)
    
    car_code = car_data['car_code']
    brand = car_data['brand']
    model = car_data['model']
    variant = car_data['variant']
    photo_url = car_data['photo_url']
    
    # Nome do ficheiro
    if variant:
        safe_name = f"{car_code}_{brand}_{model}_{variant}"
    else:
        safe_name = f"{car_code}_{brand}_{model}"
    
    safe_name = safe_name.replace(' ', '_').replace(',', '')
    safe_name = re.sub(r'[^\w\s-]', '', safe_name)
    
    # Extensão
    ext = '.jpg'
    if '.' in photo_url:
        url_ext = photo_url.split('.')[-1].split('?')[0].lower()
        if url_ext in ['jpg', 'jpeg', 'png', 'webp', 'gif']:
            ext = f'.{url_ext}'
    
    filename = f"{safe_name}{ext}"
    filepath = os.path.join(output_dir, filename)
    
    # Verificar se já existe
    if os.path.exists(filepath):
        file_size = os.path.getsize(filepath)
        if file_size > 1024:  # Maior que 1KB
            print(f"  ⏭️  Já existe: {filename} ({file_size:,} bytes)")
            return filepath
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X)',
            'Referer': 'https://www.carjet.com/',
        }
        
        response = requests.get(photo_url, headers=headers, timeout=30)
        response.raise_for_status()
        
        with open(filepath, 'wb') as f:
            f.write(response.content)
        
        file_size = len(response.content)
        
        if file_size < 1024:
            print(f"  ⚠️ Placeholder: {filename} ({file_size} bytes)")
            os.remove(filepath)
            return None
        else:
            print(f"  ✅ Download: {filename} ({file_size:,} bytes)")
            return filepath
        
    except Exception as e:
        print(f"  ❌ Erro: {e}")
        return None


def main():
    print("=" * 80)
    print("📥 DOWNLOAD DE FOTOS REAIS (do HTML renderizado)")
    print("=" * 80)
    
    # Carregar JSON
    json_file = 'carjet_cars_from_html.json'
    
    if not os.path.exists(json_file):
        print(f"\n❌ Ficheiro não encontrado: {json_file}")
        print("Execute primeiro: python3 extract_from_rendered_html.py")
        return
    
    with open(json_file, 'r', encoding='utf-8') as f:
        all_cars = json.load(f)
    
    # Remover duplicados por código
    unique_cars = {}
    for car in all_cars:
        code = car['car_code']
        if code not in unique_cars:
            unique_cars[code] = car
    
    cars_list = list(unique_cars.values())
    
    print(f"\n📊 Total de fotos únicas: {len(cars_list)}")
    print()
    
    successful = 0
    failed = 0
    
    for idx, car in enumerate(cars_list, 1):
        variant_info = f" [{car['variant']}]" if car['variant'] else ""
        print(f"[{idx}/{len(cars_list)}] {car['brand']} {car['model']}{variant_info} (Código: {car['car_code']})")
        
        result = download_photo(car)
        
        if result:
            successful += 1
        else:
            failed += 1
        
        if idx < len(cars_list):
            time.sleep(0.2)
    
    print()
    print("=" * 80)
    print("📊 RESULTADO FINAL")
    print("=" * 80)
    print(f"✅ Downloads bem-sucedidos: {successful}")
    print(f"❌ Falhas: {failed}")
    print(f"📁 Pasta: carjet_photos_real/")
    print("=" * 80)


if __name__ == '__main__':
    main()
