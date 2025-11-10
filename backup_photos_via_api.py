#!/usr/bin/env python3
"""
Backup das fotos via API do Admin (método mais simples)
Não requer DATABASE_URL, apenas credenciais de admin
"""

import requests
import json
import base64
from datetime import datetime
from pathlib import Path

# Configuração
BASE_URL = "https://carrental-api-5f8q.onrender.com"
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin"  # Alterar se necessário

BACKUP_DIR = Path("backups/vehicle_photos_api")
TIMESTAMP = datetime.now().strftime("%Y%m%d_%H%M%S")

def create_backup_dirs():
    """Criar estrutura de pastas para backup"""
    backup_path = BACKUP_DIR / TIMESTAMP
    photos_dir = backup_path / "photos"
    images_dir = backup_path / "images"
    
    photos_dir.mkdir(parents=True, exist_ok=True)
    images_dir.mkdir(parents=True, exist_ok=True)
    
    return backup_path, photos_dir, images_dir

def login_admin(session):
    """Fazer login no admin"""
    print("\n🔐 A fazer login no admin...")
    
    response = session.post(
        f"{BASE_URL}/login",
        data={
            "username": ADMIN_USERNAME,
            "password": ADMIN_PASSWORD
        },
        allow_redirects=True  # Seguir redirects
    )
    
    # Verificar se temos cookies de sessão (sinal de login bem-sucedido)
    has_session = len(session.cookies) > 0
    
    if has_session or response.status_code == 200:
        print(f"✅ Login bem-sucedido! (cookies: {len(session.cookies)})")
        return True
    else:
        print(f"❌ Login falhou: {response.status_code}")
        print(f"   Cookies: {len(session.cookies)}")
        print(f"   URL final: {response.url}")
        return False

def export_config(session):
    """Exportar configuração completa via API"""
    print("\n📥 A descarregar configuração do Render...")
    
    response = session.get(f"{BASE_URL}/api/export/config", timeout=120)
    
    if response.status_code == 200:
        print("✅ Configuração descarregada!")
        return response.json()
    else:
        print(f"❌ Erro ao exportar: {response.status_code}")
        print(f"   Resposta: {response.text[:200]}")
        return None

def extract_photos(config, photos_dir):
    """Extrair fotos do JSON para ficheiros individuais"""
    print("\n📸 A extrair fotos individuais...")
    
    photos_data = config.get("data", {}).get("photos", {})
    count = 0
    
    for vehicle_name, photo_info in photos_data.items():
        try:
            # Decodificar base64
            photo_bytes = base64.b64decode(photo_info["data"])
            
            # Determinar extensão
            content_type = photo_info.get("content_type", "image/jpeg")
            ext = content_type.split('/')[-1] if '/' in content_type else 'jpg'
            if ext == 'jpeg':
                ext = 'jpg'
            
            # Salvar ficheiro
            filename = f"{vehicle_name.replace(' ', '_').replace('/', '_')}.{ext}"
            filepath = photos_dir / filename
            
            with open(filepath, 'wb') as f:
                f.write(photo_bytes)
            
            count += 1
            size_kb = len(photo_bytes) // 1024
            print(f"   ✅ {vehicle_name} ({size_kb} KB)")
            
        except Exception as e:
            print(f"   ❌ Erro ao extrair {vehicle_name}: {e}")
    
    print(f"\n✅ {count} fotos extraídas")
    return count

def extract_images(config, images_dir):
    """Extrair imagens do JSON para ficheiros individuais"""
    print("\n🖼️  A extrair imagens individuais...")
    
    images_data = config.get("data", {}).get("images", {})
    count = 0
    
    for vehicle_key, image_info in images_data.items():
        try:
            # Decodificar base64
            image_bytes = base64.b64decode(image_info["data"])
            
            # Determinar extensão
            content_type = image_info.get("content_type", "image/jpeg")
            ext = content_type.split('/')[-1] if '/' in content_type else 'jpg'
            if ext == 'jpeg':
                ext = 'jpg'
            
            # Salvar ficheiro
            filename = f"{vehicle_key.replace(' ', '_').replace('/', '_')}.{ext}"
            filepath = images_dir / filename
            
            with open(filepath, 'wb') as f:
                f.write(image_bytes)
            
            count += 1
            size_kb = len(image_bytes) // 1024
            print(f"   ✅ {vehicle_key} ({size_kb} KB)")
            
        except Exception as e:
            print(f"   ❌ Erro ao extrair {vehicle_key}: {e}")
    
    print(f"\n✅ {count} imagens extraídas")
    return count

def main():
    """Executar backup completo via API"""
    print("=" * 70)
    print("🚗 BACKUP DE FOTOS VIA API (SEM DATABASE_URL)")
    print("=" * 70)
    print(f"\n🌐 URL: {BASE_URL}")
    
    # Criar estrutura de pastas
    backup_path, photos_dir, images_dir = create_backup_dirs()
    print(f"📁 Pasta de backup: {backup_path}")
    
    # Criar sessão
    session = requests.Session()
    
    try:
        # Login
        if not login_admin(session):
            print("\n❌ Não foi possível fazer login")
            return
        
        # Exportar configuração
        config = export_config(session)
        
        if not config:
            print("\n❌ Não foi possível exportar configuração")
            return
        
        # Salvar JSON completo
        json_path = backup_path / "backup_complete.json"
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        print(f"\n💾 JSON completo guardado: {json_path}")
        
        # Extrair fotos individuais
        photos_count = extract_photos(config, photos_dir)
        
        # Extrair imagens individuais
        images_count = extract_images(config, images_dir)
        
        # Estatísticas
        stats = config.get("statistics", {})
        
        print("\n" + "=" * 70)
        print("✅ BACKUP COMPLETO!")
        print("=" * 70)
        print(f"\n📊 ESTATÍSTICAS:")
        print(f"   - Fotos (vehicle_photos): {photos_count}")
        print(f"   - Imagens (vehicle_images): {images_count}")
        print(f"   - Veículos parametrizados: {stats.get('vehicles_count', 0)}")
        print(f"   - Grupos de carros: {stats.get('car_groups_count', 0)}")
        print(f"   - Tamanho fotos: {stats.get('total_photo_size_mb', 0):.2f} MB")
        print(f"   - Tamanho imagens: {stats.get('total_image_size_mb', 0):.2f} MB")
        
        total_size = stats.get('total_photo_size_mb', 0) + stats.get('total_image_size_mb', 0)
        print(f"   - Tamanho total: {total_size:.2f} MB")
        
        print(f"\n📁 FICHEIROS CRIADOS:")
        print(f"   - JSON completo: {json_path}")
        print(f"   - Fotos individuais: {photos_dir}/ ({photos_count} ficheiros)")
        print(f"   - Imagens individuais: {images_dir}/ ({images_count} ficheiros)")
        
        print("\n💡 DICA: Guarda o ficheiro backup_complete.json em local seguro!")
        print("   Este ficheiro contém TODAS as configurações e fotos do sistema.")
        print("=" * 70)
        
    except requests.exceptions.RequestException as e:
        print(f"\n❌ Erro de conexão: {e}")
    except Exception as e:
        print(f"\n❌ ERRO durante backup: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
