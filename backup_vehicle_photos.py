#!/usr/bin/env python3
"""
Backup completo de todas as fotos dos veículos
Extrai fotos de vehicle_photos e vehicle_images e guarda em:
1. JSON com base64 (restauração rápida)
2. Ficheiros individuais (visualização fácil)
"""

import sqlite3
import base64
import json
import os
from datetime import datetime
from pathlib import Path

# Configuração
DB_PATH = "data.db"
BACKUP_DIR = Path("backups/vehicle_photos")
TIMESTAMP = datetime.now().strftime("%Y%m%d_%H%M%S")

def create_backup_dirs():
    """Criar estrutura de pastas para backup"""
    backup_path = BACKUP_DIR / TIMESTAMP
    photos_dir = backup_path / "photos"
    images_dir = backup_path / "images"
    
    photos_dir.mkdir(parents=True, exist_ok=True)
    images_dir.mkdir(parents=True, exist_ok=True)
    
    return backup_path, photos_dir, images_dir

def backup_vehicle_photos(conn, photos_dir):
    """Backup da tabela vehicle_photos"""
    print("\n📸 BACKING UP VEHICLE_PHOTOS...")
    
    cursor = conn.execute("""
        SELECT vehicle_name, photo_data, content_type, photo_url, uploaded_at
        FROM vehicle_photos
        ORDER BY vehicle_name
    """)
    
    photos_data = {}
    count = 0
    
    for row in cursor:
        vehicle_name = row[0]
        photo_data = row[1]
        content_type = row[2] or "image/jpeg"
        photo_url = row[3]
        uploaded_at = row[4]
        
        if photo_data:
            # Determinar extensão
            ext = content_type.split('/')[-1] if '/' in content_type else 'jpg'
            if ext == 'jpeg':
                ext = 'jpg'
            
            # Salvar ficheiro individual
            filename = f"{vehicle_name.replace(' ', '_').replace('/', '_')}.{ext}"
            filepath = photos_dir / filename
            
            with open(filepath, 'wb') as f:
                f.write(photo_data)
            
            # Adicionar ao JSON (base64)
            photo_base64 = base64.b64encode(photo_data).decode('utf-8')
            photos_data[vehicle_name] = {
                "data": photo_base64,
                "content_type": content_type,
                "url": photo_url,
                "uploaded_at": uploaded_at,
                "size_bytes": len(photo_data),
                "filename": filename
            }
            
            count += 1
            print(f"   ✅ {vehicle_name} ({len(photo_data) // 1024} KB)")
    
    print(f"\n✅ {count} fotos guardadas em vehicle_photos")
    return photos_data

def backup_vehicle_images(conn, images_dir):
    """Backup da tabela vehicle_images"""
    print("\n🖼️  BACKING UP VEHICLE_IMAGES...")
    
    cursor = conn.execute("""
        SELECT vehicle_key, image_data, content_type, source_url, downloaded_at
        FROM vehicle_images
        ORDER BY vehicle_key
    """)
    
    images_data = {}
    count = 0
    
    for row in cursor:
        vehicle_key = row[0]
        image_data = row[1]
        content_type = row[2] or "image/jpeg"
        source_url = row[3]
        downloaded_at = row[4]
        
        if image_data:
            # Determinar extensão
            ext = content_type.split('/')[-1] if '/' in content_type else 'jpg'
            if ext == 'jpeg':
                ext = 'jpg'
            
            # Salvar ficheiro individual
            filename = f"{vehicle_key.replace(' ', '_').replace('/', '_')}.{ext}"
            filepath = images_dir / filename
            
            with open(filepath, 'wb') as f:
                f.write(image_data)
            
            # Adicionar ao JSON (base64)
            image_base64 = base64.b64encode(image_data).decode('utf-8')
            images_data[vehicle_key] = {
                "data": image_base64,
                "content_type": content_type,
                "source_url": source_url,
                "downloaded_at": downloaded_at,
                "size_bytes": len(image_data),
                "filename": filename
            }
            
            count += 1
            print(f"   ✅ {vehicle_key} ({len(image_data) // 1024} KB)")
    
    print(f"\n✅ {count} imagens guardadas em vehicle_images")
    return images_data

def main():
    """Executar backup completo"""
    print("=" * 70)
    print("🚗 BACKUP COMPLETO DE FOTOS DOS VEÍCULOS")
    print("=" * 70)
    
    # Verificar se DB existe
    if not os.path.exists(DB_PATH):
        print(f"❌ Base de dados não encontrada: {DB_PATH}")
        return
    
    # Criar estrutura de pastas
    backup_path, photos_dir, images_dir = create_backup_dirs()
    print(f"\n📁 Pasta de backup: {backup_path}")
    
    # Conectar à base de dados
    conn = sqlite3.connect(DB_PATH)
    
    try:
        # Backup vehicle_photos
        photos_data = backup_vehicle_photos(conn, photos_dir)
        
        # Backup vehicle_images
        images_data = backup_vehicle_images(conn, images_dir)
        
        # Criar JSON completo
        backup_json = {
            "backup_date": datetime.now().isoformat(),
            "database": DB_PATH,
            "statistics": {
                "total_photos": len(photos_data),
                "total_images": len(images_data),
                "photos_size_mb": sum(p["size_bytes"] for p in photos_data.values()) / (1024 * 1024),
                "images_size_mb": sum(i["size_bytes"] for i in images_data.values()) / (1024 * 1024)
            },
            "vehicle_photos": photos_data,
            "vehicle_images": images_data
        }
        
        # Salvar JSON
        json_path = backup_path / "backup_complete.json"
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(backup_json, f, indent=2, ensure_ascii=False)
        
        print("\n" + "=" * 70)
        print("✅ BACKUP COMPLETO!")
        print("=" * 70)
        print(f"\n📊 ESTATÍSTICAS:")
        print(f"   - Fotos (vehicle_photos): {len(photos_data)}")
        print(f"   - Imagens (vehicle_images): {len(images_data)}")
        print(f"   - Tamanho total: {backup_json['statistics']['photos_size_mb'] + backup_json['statistics']['images_size_mb']:.2f} MB")
        print(f"\n📁 FICHEIROS CRIADOS:")
        print(f"   - JSON completo: {json_path}")
        print(f"   - Fotos individuais: {photos_dir}/ ({len(photos_data)} ficheiros)")
        print(f"   - Imagens individuais: {images_dir}/ ({len(images_data)} ficheiros)")
        print("\n💡 Para restaurar, use o ficheiro backup_complete.json")
        print("=" * 70)
        
    finally:
        conn.close()

if __name__ == "__main__":
    main()
