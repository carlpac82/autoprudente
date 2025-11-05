#!/usr/bin/env python3
"""
Upload de fotos de veículos dos ficheiros locais para o Render
"""

import requests
from pathlib import Path
import sys

# Configuração
RENDER_URL = "https://carrental-api-9f8q.onrender.com"
PHOTOS_DIR = Path(__file__).parent / "carjet_photos"

# Credenciais (admin/admin)
USERNAME = "admin"
PASSWORD = "admin"

# Mapeamento de nomes de ficheiros para nomes de veículos na BD
VEHICLE_MAPPING = {
    "Fiat_500.jpg": "fiat 500",
    "Fiat_Panda.jpg": "fiat panda",
    "Opel_Corsa.jpg": "opel corsa",
    "Opel_Mokka__Electric.jpg": "opel mokka electric",
    "Peugeot_2008.jpg": "peugeot 2008",
    "Peugeot_308.jpg": "peugeot 308",
    "Renault_Clio.jpg": "renault clio",
    "Renault_Megane.jpg": "renault megane",
    "VW_Golf.jpg": "volkswagen golf",
    "VW_Polo.jpg": "volkswagen polo",
}

def login():
    """Faz login e retorna a sessão autenticada"""
    session = requests.Session()
    
    # Fazer login via form
    login_url = f"{RENDER_URL}/login"
    data = {
        "username": USERNAME,
        "password": PASSWORD
    }
    
    response = session.post(login_url, data=data, timeout=30, allow_redirects=False)
    
    print(f"   Status: {response.status_code}")
    print(f"   Cookies: {session.cookies.get_dict()}")
    
    # Verificar se tem cookie de sessão
    if session.cookies.get('session') or response.status_code in [200, 302, 303]:
        print("✅ Login efetuado com sucesso")
        return session
    else:
        print(f"❌ Erro no login: HTTP {response.status_code}")
        print(f"   Response: {response.text[:200]}")
        return None

def upload_photo(session, vehicle_name, photo_path):
    """Faz upload de uma foto para o Render"""
    try:
        # Endpoint temporário SEM autenticação
        url = f"{RENDER_URL}/api/temp/upload-photo/{vehicle_name}"
        
        # Ler ficheiro
        with open(photo_path, 'rb') as f:
            files = {
                'file': (photo_path.name, f, 'image/jpeg')
            }
            
            # Fazer upload com sessão autenticada
            response = session.post(url, files=files, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('ok'):
                print(f"✅ {vehicle_name:30s} ({photo_path.name})")
                return True
            else:
                print(f"❌ {vehicle_name:30s}: {data.get('error', 'Unknown error')}")
                return False
        else:
            print(f"❌ {vehicle_name:30s}: HTTP {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ {vehicle_name:30s}: {e}")
        return False

def main():
    print("=" * 80)
    print("📸 UPLOAD DE FOTOS PARA O RENDER")
    print("=" * 80)
    print()
    
    # Fazer login
    print("🔐 A fazer login...")
    session = login()
    if not session:
        print("❌ Não foi possível fazer login. Abortando.")
        return
    print()
    
    # Verificar se a pasta existe
    if not PHOTOS_DIR.exists():
        print(f"❌ Pasta não encontrada: {PHOTOS_DIR}")
        return
    
    # Listar fotos disponíveis
    available_photos = list(PHOTOS_DIR.glob("*.jpg"))
    print(f"🔍 Encontradas {len(available_photos)} fotos em {PHOTOS_DIR.name}/")
    print()
    
    # Upload de cada foto
    print("📤 A fazer upload das fotos...")
    print("-" * 80)
    
    success = 0
    failed = 0
    skipped = 0
    
    for photo_path in available_photos:
        filename = photo_path.name
        
        if filename in VEHICLE_MAPPING:
            vehicle_name = VEHICLE_MAPPING[filename]
            if upload_photo(session, vehicle_name, photo_path):
                success += 1
            else:
                failed += 1
        else:
            print(f"⏭️  {filename:30s} (sem mapeamento)")
            skipped += 1
    
    print()
    print("=" * 80)
    print(f"✅ Sucesso: {success} | ❌ Falhas: {failed} | ⏭️  Ignoradas: {skipped}")
    print("=" * 80)

if __name__ == "__main__":
    main()
