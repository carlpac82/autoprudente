#!/usr/bin/env python3
"""
Importa as 57 fotos reais para a base de dados
"""

import json
import sqlite3
import os
from datetime import datetime

def import_photos_to_db():
    """Importa fotos para vehicle_photos"""
    
    print("=" * 80)
    print("📥 IMPORTAÇÃO DE 57 FOTOS PARA BASE DE DADOS")
    print("=" * 80)
    
    # Carregar lista de fotos
    with open('carjet_photos_for_import.json', 'r', encoding='utf-8') as f:
        photos = json.load(f)
    
    print(f"\n📊 Total de fotos a importar: {len(photos)}")
    
    # Conectar à BD
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    
    # Garantir que tabela existe
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS vehicle_photos (
            vehicle_name TEXT PRIMARY KEY,
            photo_data BLOB,
            photo_url TEXT,
            content_type TEXT DEFAULT 'image/jpeg',
            uploaded_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    imported = 0
    skipped = 0
    errors = 0
    
    for idx, photo in enumerate(photos, 1):
        car_name = photo['name']
        photo_file = photo['photo_file']
        photo_url = photo['photo_url']
        category = photo['category']
        
        print(f"\n[{idx}/{len(photos)}] {car_name} ({category})")
        
        # Verificar se ficheiro existe
        if not os.path.exists(photo_file):
            print(f"  ⚠️ Ficheiro não encontrado: {photo_file}")
            skipped += 1
            continue
        
        try:
            # Ler foto
            with open(photo_file, 'rb') as f:
                photo_data = f.read()
            
            file_size = len(photo_data)
            
            # Verificar se é placeholder
            if file_size < 1024:
                print(f"  ⏭️  Placeholder ignorado ({file_size} bytes)")
                skipped += 1
                continue
            
            # Inserir ou atualizar
            cursor.execute("""
                INSERT OR REPLACE INTO vehicle_photos 
                (vehicle_name, photo_data, photo_url, content_type, uploaded_at)
                VALUES (?, ?, ?, 'image/jpeg', ?)
            """, (car_name, photo_data, photo_url, datetime.now().isoformat()))
            
            conn.commit()
            imported += 1
            
            print(f"  ✅ Importada: {file_size:,} bytes")
            
        except Exception as e:
            print(f"  ❌ Erro: {e}")
            errors += 1
            continue
    
    conn.close()
    
    print("\n" + "=" * 80)
    print("📊 RESULTADO DA IMPORTAÇÃO")
    print("=" * 80)
    print(f"✅ Importadas: {imported}")
    print(f"⏭️  Ignoradas: {skipped}")
    print(f"❌ Erros: {errors}")
    print("=" * 80)


if __name__ == '__main__':
    import_photos_to_db()
