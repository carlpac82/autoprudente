#!/usr/bin/env python3
"""
Upload DIRETO de fotos para o PostgreSQL do Render
Bypassa a API e escreve diretamente na base de dados
"""

import psycopg2
from pathlib import Path
import re
import sys

# Connection string do Render PostgreSQL
DATABASE_URL = "postgresql://carrental_user:cmXcauHIuQinAyDQjcB9XiVMU0Gaxviz@dpg-d44gvnm3jp1c73dc2edg-a.frankfurt-postgres.render.com/carrental_db_9klo"

PHOTOS_DIRS = [
    Path(__file__).parent / "carjet_photos",
    Path(__file__).parent / "carjet_photos_by_group"
]

def clean_vehicle_name(filename):
    """Extrai o nome do veículo do nome do ficheiro"""
    name = filename.replace('.jpg', '').replace('.png', '')
    name = re.sub(r'^[A-Z]\d+_', '', name)
    name = name.replace('_', ' ')
    name = name.lower().strip()
    name = name.replace('vw ', 'volkswagen ')
    return name

def ensure_tables(conn):
    """Garante que as tabelas existem"""
    cursor = conn.cursor()
    
    # Tabela vehicle_photos
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS vehicle_photos (
            vehicle_name TEXT PRIMARY KEY,
            photo_data BYTEA,
            photo_url TEXT,
            content_type TEXT,
            uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Tabela vehicle_images
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS vehicle_images (
            vehicle_key TEXT PRIMARY KEY,
            image_data BYTEA NOT NULL,
            content_type TEXT DEFAULT 'image/jpeg',
            downloaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    conn.commit()
    print("✅ Tabelas verificadas/criadas")

def upload_photo(conn, vehicle_name, photo_path):
    """Faz upload de uma foto diretamente para o PostgreSQL"""
    try:
        # Ler ficheiro
        with open(photo_path, 'rb') as f:
            photo_data = f.read()
        
        content_type = 'image/jpeg'
        vehicle_key = vehicle_name.lower().strip()
        
        cursor = conn.cursor()
        
        # Inserir em vehicle_photos
        cursor.execute("""
            INSERT INTO vehicle_photos (vehicle_name, photo_data, content_type, photo_url)
            VALUES (%s, %s, %s, NULL)
            ON CONFLICT (vehicle_name) 
            DO UPDATE SET photo_data = EXCLUDED.photo_data, 
                         content_type = EXCLUDED.content_type
        """, (vehicle_key, photo_data, content_type))
        
        # Inserir em vehicle_images
        cursor.execute("""
            INSERT INTO vehicle_images (vehicle_key, image_data, content_type)
            VALUES (%s, %s, %s)
            ON CONFLICT (vehicle_key)
            DO UPDATE SET image_data = EXCLUDED.image_data,
                         content_type = EXCLUDED.content_type
        """, (vehicle_key, photo_data, content_type))
        
        conn.commit()
        return True, "OK"
        
    except Exception as e:
        conn.rollback()
        return False, str(e)

def main():
    print("=" * 80)
    print("📸 UPLOAD DIRETO DE FOTOS PARA POSTGRESQL DO RENDER")
    print("=" * 80)
    print()
    
    # Conectar ao PostgreSQL
    print("🔌 A conectar ao PostgreSQL...")
    try:
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        print("✅ Conectado com sucesso!")
        print()
    except Exception as e:
        print(f"❌ Erro ao conectar: {e}")
        return
    
    # Garantir que as tabelas existem
    ensure_tables(conn)
    print()
    
    # Coletar todas as fotos
    all_photos = []
    for photos_dir in PHOTOS_DIRS:
        if photos_dir.exists():
            all_photos.extend(photos_dir.rglob("*.jpg"))
            all_photos.extend(photos_dir.rglob("*.png"))
    
    print(f"🔍 Encontradas {len(all_photos)} fotos")
    print()
    
    # Upload de cada foto
    print("📤 A fazer upload das fotos...")
    print("-" * 80)
    
    success = 0
    failed = 0
    
    for photo_path in sorted(all_photos):
        vehicle_name = clean_vehicle_name(photo_path.name)
        ok, msg = upload_photo(conn, vehicle_name, photo_path)
        
        if ok:
            print(f"✅ {vehicle_name:35s} ({len(open(photo_path, 'rb').read())} bytes)")
            success += 1
        else:
            print(f"❌ {vehicle_name:35s} - {msg}")
            failed += 1
    
    conn.close()
    
    print()
    print("=" * 80)
    print(f"✅ Sucesso: {success} | ❌ Falhas: {failed}")
    print("=" * 80)

if __name__ == "__main__":
    main()
