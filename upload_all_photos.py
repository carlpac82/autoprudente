#!/usr/bin/env python3
"""
Upload de TODAS as fotos de veículos para o Render
Processa automaticamente os nomes dos ficheiros
"""

import requests
from pathlib import Path
import re

# Configuração
RENDER_URL = "https://carrental-api-9f8q.onrender.com"
PHOTOS_DIRS = [
    Path(__file__).parent / "carjet_photos",
    Path(__file__).parent / "carjet_photos_by_group"
]

def clean_vehicle_name(filename):
    """Extrai o nome do veículo do nome do ficheiro"""
    # Remover extensão
    name = filename.replace('.jpg', '').replace('.png', '')
    
    # Remover código inicial (ex: C04_, A273_, etc)
    name = re.sub(r'^[A-Z]\d+_', '', name)
    
    # Substituir underscores por espaços
    name = name.replace('_', ' ')
    
    # Converter para minúsculas
    name = name.lower().strip()
    
    # Casos especiais
    name = name.replace('vw ', 'volkswagen ')
    
    return name

def upload_photo(vehicle_name, photo_path):
    """Faz upload de uma foto para o Render"""
    try:
        # Endpoint temporário SEM autenticação
        url = f"{RENDER_URL}/api/temp/upload-photo/{vehicle_name}"
        
        # Ler ficheiro
        with open(photo_path, 'rb') as f:
            files = {
                'file': (photo_path.name, f, 'image/jpeg')
            }
            
            # Fazer upload
            response = requests.post(url, files=files, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('ok'):
                return True, "OK"
            else:
                return False, data.get('error', 'Unknown error')
        else:
            return False, f"HTTP {response.status_code}"
            
    except Exception as e:
        return False, str(e)

def main():
    print("=" * 80)
    print("📸 UPLOAD DE TODAS AS FOTOS PARA O RENDER")
    print("=" * 80)
    print()
    
    # Coletar todas as fotos
    all_photos = []
    for photos_dir in PHOTOS_DIRS:
        if photos_dir.exists():
            # Buscar recursivamente
            all_photos.extend(photos_dir.rglob("*.jpg"))
            all_photos.extend(photos_dir.rglob("*.png"))
    
    print(f"🔍 Encontradas {len(all_photos)} fotos")
    print()
    
    # Upload de cada foto
    print("📤 A fazer upload das fotos...")
    print("-" * 80)
    
    success = 0
    failed = 0
    failed_list = []
    
    for photo_path in sorted(all_photos):
        vehicle_name = clean_vehicle_name(photo_path.name)
        ok, msg = upload_photo(vehicle_name, photo_path)
        
        if ok:
            print(f"✅ {vehicle_name:35s} ({photo_path.name})")
            success += 1
        else:
            print(f"❌ {vehicle_name:35s} - {msg}")
            failed += 1
            failed_list.append((vehicle_name, msg))
    
    print()
    print("=" * 80)
    print(f"✅ Sucesso: {success} | ❌ Falhas: {failed}")
    print("=" * 80)
    
    if failed_list:
        print()
        print("Fotos que falharam:")
        for name, error in failed_list[:10]:
            print(f"  - {name}: {error}")
        if len(failed_list) > 10:
            print(f"  ... e mais {len(failed_list) - 10}")

if __name__ == "__main__":
    main()
