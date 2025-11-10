#!/usr/bin/env python3
"""
Backup das fotos diretamente do PostgreSQL do Render
Usa a DATABASE_URL do ambiente ou .env
"""

import os
import sys
import base64
import json
from datetime import datetime
from pathlib import Path

try:
    import psycopg2
except ImportError:
    print("❌ psycopg2 não instalado!")
    print("💡 Instale com: pip install psycopg2-binary")
    sys.exit(1)

# Tentar carregar DATABASE_URL
DATABASE_URL = os.environ.get('DATABASE_URL')

if not DATABASE_URL:
    try:
        from dotenv import load_dotenv
        load_dotenv()
        DATABASE_URL = os.environ.get('DATABASE_URL')
    except:
        pass

if not DATABASE_URL:
    print("❌ DATABASE_URL não encontrada!")
    print("💡 Defina a variável de ambiente DATABASE_URL ou crie um ficheiro .env")
    print("\nExemplo:")
    print("export DATABASE_URL='postgresql://user:pass@host:5432/dbname'")
    sys.exit(1)

# Configuração
BACKUP_DIR = Path("backups/vehicle_photos_render")
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
    print("\n📸 BACKING UP VEHICLE_PHOTOS (PostgreSQL)...")
    
    cursor = conn.cursor()
    cursor.execute("""
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
            # photo_data já é bytes no PostgreSQL
            photo_bytes = bytes(photo_data) if not isinstance(photo_data, bytes) else photo_data
            
            # Determinar extensão
            ext = content_type.split('/')[-1] if '/' in content_type else 'jpg'
            if ext == 'jpeg':
                ext = 'jpg'
            
            # Salvar ficheiro individual
            filename = f"{vehicle_name.replace(' ', '_').replace('/', '_')}.{ext}"
            filepath = photos_dir / filename
            
            with open(filepath, 'wb') as f:
                f.write(photo_bytes)
            
            # Adicionar ao JSON (base64)
            photo_base64 = base64.b64encode(photo_bytes).decode('utf-8')
            uploaded_at_str = uploaded_at.isoformat() if uploaded_at else None
            
            photos_data[vehicle_name] = {
                "data": photo_base64,
                "content_type": content_type,
                "url": photo_url,
                "uploaded_at": uploaded_at_str,
                "size_bytes": len(photo_bytes),
                "filename": filename
            }
            
            count += 1
            size_kb = len(photo_bytes) // 1024
            print(f"   ✅ {vehicle_name} ({size_kb} KB)")
    
    cursor.close()
    print(f"\n✅ {count} fotos guardadas em vehicle_photos")
    return photos_data

def backup_vehicle_images(conn, images_dir):
    """Backup da tabela vehicle_images"""
    print("\n🖼️  BACKING UP VEHICLE_IMAGES (PostgreSQL)...")
    
    cursor = conn.cursor()
    cursor.execute("""
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
            # image_data já é bytes no PostgreSQL
            image_bytes = bytes(image_data) if not isinstance(image_data, bytes) else image_data
            
            # Determinar extensão
            ext = content_type.split('/')[-1] if '/' in content_type else 'jpg'
            if ext == 'jpeg':
                ext = 'jpg'
            
            # Salvar ficheiro individual
            filename = f"{vehicle_key.replace(' ', '_').replace('/', '_')}.{ext}"
            filepath = images_dir / filename
            
            with open(filepath, 'wb') as f:
                f.write(image_bytes)
            
            # Adicionar ao JSON (base64)
            image_base64 = base64.b64encode(image_bytes).decode('utf-8')
            downloaded_at_str = downloaded_at.isoformat() if downloaded_at else None
            
            images_data[vehicle_key] = {
                "data": image_base64,
                "content_type": content_type,
                "source_url": source_url,
                "downloaded_at": downloaded_at_str,
                "size_bytes": len(image_bytes),
                "filename": filename
            }
            
            count += 1
            size_kb = len(image_bytes) // 1024
            print(f"   ✅ {vehicle_key} ({size_kb} KB)")
    
    cursor.close()
    print(f"\n✅ {count} imagens guardadas em vehicle_images")
    return images_data

def main():
    """Executar backup completo do Render"""
    print("=" * 70)
    print("🚗 BACKUP COMPLETO DE FOTOS DOS VEÍCULOS (RENDER - POSTGRESQL)")
    print("=" * 70)
    print(f"\n🔗 Conectando ao Render...")
    
    # Criar estrutura de pastas
    backup_path, photos_dir, images_dir = create_backup_dirs()
    print(f"📁 Pasta de backup: {backup_path}")
    
    # Conectar ao PostgreSQL
    try:
        conn = psycopg2.connect(DATABASE_URL)
        print("✅ Conectado ao PostgreSQL do Render!")
    except Exception as e:
        print(f"❌ Erro ao conectar: {e}")
        return
    
    try:
        # Backup vehicle_photos
        photos_data = backup_vehicle_photos(conn, photos_dir)
        
        # Backup vehicle_images
        images_data = backup_vehicle_images(conn, images_dir)
        
        # Criar JSON completo
        backup_json = {
            "backup_date": datetime.now().isoformat(),
            "database": "PostgreSQL Render",
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
        photos_mb = backup_json['statistics']['photos_size_mb']
        images_mb = backup_json['statistics']['images_size_mb']
        print(f"   - Tamanho fotos: {photos_mb:.2f} MB")
        print(f"   - Tamanho imagens: {images_mb:.2f} MB")
        print(f"   - Tamanho total: {photos_mb + images_mb:.2f} MB")
        print(f"\n📁 FICHEIROS CRIADOS:")
        print(f"   - JSON completo: {json_path}")
        print(f"   - Fotos individuais: {photos_dir}/ ({len(photos_data)} ficheiros)")
        print(f"   - Imagens individuais: {images_dir}/ ({len(images_data)} ficheiros)")
        print("\n💡 Para restaurar, use o ficheiro backup_complete.json")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n❌ ERRO durante backup: {e}")
        import traceback
        traceback.print_exc()
    finally:
        conn.close()
        print("\n🔌 Conexão fechada")

if __name__ == "__main__":
    main()
