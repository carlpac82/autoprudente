#!/usr/bin/env python3
"""
Upload das fotos REAIS (ficheiros locais) para o PostgreSQL do Render
"""
import psycopg2
import os
import sys
from pathlib import Path

# Connection string atualizada
DATABASE_URL = "postgresql://carrental_user:cmXcauHIuQinAyDQjcB9XiVMU0Gaxviz@dpg-d44gvnm3jp1c73dc2edg-a.frankfurt-postgres.render.com/carrental_db_9klo?sslmode=require"

def normalize_vehicle_name(filename):
    """Extrai e normaliza o nome do veículo do filename"""
    # Remove extensão
    name = os.path.splitext(filename)[0]
    
    # Remove códigos (C04_, GZ91_, etc)
    if '_' in name:
        parts = name.split('_')
        if len(parts[0]) <= 4 and parts[0][0].isupper():
            name = '_'.join(parts[1:])
    
    # Substitui _ por espaço e converte para lowercase
    name = name.replace('_', ' ').lower().strip()
    
    return name

try:
    print("🔍 Conectando ao PostgreSQL do Render...")
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    
    # Garantir que as tabelas existem
    print("\n📊 Criando tabelas se não existirem...")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS vehicle_images (
            vehicle_key TEXT PRIMARY KEY,
            image_data BYTEA NOT NULL,
            content_type TEXT DEFAULT 'image/jpeg',
            downloaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS vehicle_photos (
            vehicle_name TEXT PRIMARY KEY,
            photo_data BYTEA,
            photo_url TEXT,
            content_type TEXT DEFAULT 'image/jpeg',
            uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    print("✅ Tabelas criadas/verificadas")
    
    # Procurar fotos locais
    photo_dirs = ['carjet_photos', 'carjet_photos_by_group']
    uploaded = 0
    skipped = 0
    errors = 0
    
    for photo_dir in photo_dirs:
        if not os.path.exists(photo_dir):
            print(f"⚠️  Diretório {photo_dir} não encontrado")
            continue
        
        print(f"\n📁 Processando {photo_dir}...")
        
        # Procurar recursivamente
        for root, dirs, files in os.walk(photo_dir):
            for filename in files:
                if not (filename.endswith('.jpg') or filename.endswith('.png')):
                    continue
                
                filepath = os.path.join(root, filename)
                
                try:
                    # Ler ficheiro
                    with open(filepath, 'rb') as f:
                        photo_data = f.read()
                    
                    # Verificar se é placeholder (680 bytes)
                    if len(photo_data) == 680:
                        skipped += 1
                        continue
                    
                    # Extrair nome do veículo
                    vehicle_name = normalize_vehicle_name(filename)
                    
                    # Determinar content type
                    content_type = 'image/png' if filename.endswith('.png') else 'image/jpeg'
                    
                    # Inserir em vehicle_images
                    cursor.execute("""
                        INSERT INTO vehicle_images (vehicle_key, image_data, content_type)
                        VALUES (%s, %s, %s)
                        ON CONFLICT (vehicle_key)
                        DO UPDATE SET image_data = EXCLUDED.image_data,
                                     content_type = EXCLUDED.content_type
                    """, (vehicle_name, photo_data, content_type))
                    
                    # Inserir em vehicle_photos
                    cursor.execute("""
                        INSERT INTO vehicle_photos (vehicle_name, photo_data, content_type, photo_url)
                        VALUES (%s, %s, %s, NULL)
                        ON CONFLICT (vehicle_name)
                        DO UPDATE SET photo_data = EXCLUDED.photo_data,
                                     content_type = EXCLUDED.content_type
                    """, (vehicle_name, photo_data, content_type))
                    
                    uploaded += 1
                    if uploaded % 10 == 0:
                        print(f"  ✅ {uploaded} fotos enviadas... (última: {vehicle_name})")
                        conn.commit()
                    
                except Exception as e:
                    errors += 1
                    print(f"  ❌ Erro ao processar {filename}: {e}")
    
    # Commit final
    conn.commit()
    
    print(f"\n✅ Upload completo!")
    print(f"   📸 Fotos enviadas: {uploaded}")
    print(f"   ⏭️  Placeholders ignorados: {skipped}")
    print(f"   ❌ Erros: {errors}")
    
    # Verificar total
    cursor.execute("SELECT COUNT(*) FROM vehicle_images WHERE LENGTH(image_data) > 680")
    real_photos = cursor.fetchone()[0]
    print(f"\n🎉 Total de fotos REAIS no PostgreSQL: {real_photos}")
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"\n❌ ERRO: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
