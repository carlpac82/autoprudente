#!/usr/bin/env python3
"""
Restaurar fotos dos veículos a partir de um backup
Pode restaurar de:
1. JSON completo (backup_complete.json)
2. Pasta com ficheiros individuais
"""

import sqlite3
import base64
import json
import os
import sys
from pathlib import Path

DB_PATH = "data.db"

def restore_from_json(json_path):
    """Restaurar a partir do ficheiro JSON completo"""
    print(f"\n📥 A carregar backup de: {json_path}")
    
    with open(json_path, 'r', encoding='utf-8') as f:
        backup = json.load(f)
    
    print(f"   Backup criado em: {backup['backup_date']}")
    print(f"   Fotos: {backup['statistics']['total_photos']}")
    print(f"   Imagens: {backup['statistics']['total_images']}")
    print(f"   Tamanho total: {backup['statistics']['photos_size_mb'] + backup['statistics']['images_size_mb']:.2f} MB")
    
    # Confirmar
    response = input("\n❓ Deseja restaurar este backup? (s/N): ")
    if response.lower() != 's':
        print("❌ Cancelado pelo utilizador")
        return
    
    conn = sqlite3.connect(DB_PATH)
    
    try:
        # Restaurar vehicle_photos
        print("\n📸 A restaurar vehicle_photos...")
        photos_count = 0
        
        for vehicle_name, photo_info in backup['vehicle_photos'].items():
            photo_data = base64.b64decode(photo_info['data'])
            
            conn.execute("""
                INSERT OR REPLACE INTO vehicle_photos 
                (vehicle_name, photo_data, content_type, photo_url, uploaded_at)
                VALUES (?, ?, ?, ?, ?)
            """, (
                vehicle_name,
                photo_data,
                photo_info['content_type'],
                photo_info.get('url'),
                photo_info.get('uploaded_at')
            ))
            
            photos_count += 1
            print(f"   ✅ {vehicle_name}")
        
        # Restaurar vehicle_images
        print("\n🖼️  A restaurar vehicle_images...")
        images_count = 0
        
        for vehicle_key, image_info in backup['vehicle_images'].items():
            image_data = base64.b64decode(image_info['data'])
            
            conn.execute("""
                INSERT OR REPLACE INTO vehicle_images 
                (vehicle_key, image_data, content_type, source_url, downloaded_at)
                VALUES (?, ?, ?, ?, ?)
            """, (
                vehicle_key,
                image_data,
                image_info['content_type'],
                image_info.get('source_url'),
                image_info.get('downloaded_at')
            ))
            
            images_count += 1
            print(f"   ✅ {vehicle_key}")
        
        conn.commit()
        
        print("\n" + "=" * 70)
        print("✅ RESTAURO COMPLETO!")
        print("=" * 70)
        print(f"   - Fotos restauradas: {photos_count}")
        print(f"   - Imagens restauradas: {images_count}")
        print("=" * 70)
        
    except Exception as e:
        conn.rollback()
        print(f"\n❌ ERRO ao restaurar: {e}")
        import traceback
        traceback.print_exc()
    finally:
        conn.close()

def list_available_backups():
    """Listar todos os backups disponíveis"""
    backups_dir = Path("backups/vehicle_photos")
    
    if not backups_dir.exists():
        print("❌ Nenhum backup encontrado")
        return []
    
    backups = []
    for backup_path in sorted(backups_dir.iterdir(), reverse=True):
        if backup_path.is_dir():
            json_file = backup_path / "backup_complete.json"
            if json_file.exists():
                with open(json_file, 'r') as f:
                    data = json.load(f)
                backups.append({
                    "path": json_file,
                    "date": data['backup_date'],
                    "photos": data['statistics']['total_photos'],
                    "images": data['statistics']['total_images'],
                    "size_mb": data['statistics']['photos_size_mb'] + data['statistics']['images_size_mb']
                })
    
    return backups

def main():
    """Menu principal de restauro"""
    print("=" * 70)
    print("🔄 RESTAURAR FOTOS DOS VEÍCULOS")
    print("=" * 70)
    
    # Listar backups disponíveis
    backups = list_available_backups()
    
    if not backups:
        print("\n❌ Nenhum backup disponível")
        print("💡 Execute primeiro: python backup_vehicle_photos.py")
        return
    
    print(f"\n📋 BACKUPS DISPONÍVEIS ({len(backups)}):\n")
    
    for i, backup in enumerate(backups, 1):
        print(f"{i}. {backup['date']}")
        print(f"   - Fotos: {backup['photos']} | Imagens: {backup['images']}")
        print(f"   - Tamanho: {backup['size_mb']:.2f} MB")
        print(f"   - Ficheiro: {backup['path']}")
        print()
    
    # Escolher backup
    try:
        choice = input(f"📥 Escolha o backup para restaurar (1-{len(backups)}) ou 'q' para sair: ")
        
        if choice.lower() == 'q':
            print("👋 Cancelado")
            return
        
        index = int(choice) - 1
        if 0 <= index < len(backups):
            restore_from_json(backups[index]['path'])
        else:
            print("❌ Opção inválida")
    
    except ValueError:
        print("❌ Entrada inválida")
    except KeyboardInterrupt:
        print("\n\n👋 Cancelado pelo utilizador")

if __name__ == "__main__":
    main()
