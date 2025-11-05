#!/usr/bin/env python3
"""
Upload de fotos de veículos da base local para o Render (PostgreSQL)
"""

import sqlite3
import requests
import sys
from pathlib import Path

# Configuração
RENDER_URL = "https://carrental-api-9f8q.onrender.com"  # Ajusta se necessário
LOCAL_DB = Path(__file__).parent / "data.db"

def get_local_photos():
    """Busca todas as fotos da base de dados local"""
    conn = sqlite3.connect(LOCAL_DB)
    cursor = conn.execute("""
        SELECT vehicle_name, photo_data, photo_url, content_type 
        FROM vehicle_photos
        WHERE photo_data IS NOT NULL
    """)
    photos = cursor.fetchall()
    conn.close()
    return photos

def upload_photo(vehicle_name, photo_data, photo_url, content_type):
    """Faz upload de uma foto para o Render"""
    try:
        # Endpoint de upload
        url = f"{RENDER_URL}/api/vehicles/{vehicle_name}/photo/upload"
        
        # Criar ficheiro em memória
        files = {
            'file': (f'{vehicle_name}.jpg', photo_data, content_type or 'image/jpeg')
        }
        
        # Fazer upload
        response = requests.post(url, files=files, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('ok'):
                print(f"✅ {vehicle_name}")
                return True
            else:
                print(f"❌ {vehicle_name}: {data.get('error', 'Unknown error')}")
                return False
        else:
            print(f"❌ {vehicle_name}: HTTP {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ {vehicle_name}: {e}")
        return False

def main():
    print("=" * 80)
    print("📸 UPLOAD DE FOTOS PARA O RENDER")
    print("=" * 80)
    print()
    
    # Buscar fotos locais
    print("🔍 A buscar fotos na base de dados local...")
    photos = get_local_photos()
    print(f"   Encontradas {len(photos)} fotos")
    print()
    
    if not photos:
        print("⚠️  Nenhuma foto encontrada na base de dados local")
        return
    
    # Upload de cada foto
    print("📤 A fazer upload das fotos...")
    print("-" * 80)
    
    success = 0
    failed = 0
    
    for vehicle_name, photo_data, photo_url, content_type in photos:
        if upload_photo(vehicle_name, photo_data, photo_url, content_type):
            success += 1
        else:
            failed += 1
    
    print()
    print("=" * 80)
    print(f"✅ Upload concluído: {success} sucesso, {failed} falhas")
    print("=" * 80)

if __name__ == "__main__":
    main()
