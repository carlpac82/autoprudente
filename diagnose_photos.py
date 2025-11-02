#!/usr/bin/env python3
"""
Diagnóstico de Fotos dos Carros
Verifica quais fotos estão disponíveis no car_images.db e quais faltam
"""

import sqlite3
import os
from pathlib import Path

def main():
    # Caminho para car_images.db
    car_images_db = Path(__file__).parent / "car_images.db"
    
    if not car_images_db.exists():
        print(f"❌ Base de dados não encontrada: {car_images_db}")
        return
    
    print(f"✅ Base de dados encontrada: {car_images_db}")
    print(f"📊 Tamanho: {car_images_db.stat().st_size / 1024:.2f} KB\n")
    
    # Conectar à base de dados
    conn = sqlite3.connect(str(car_images_db))
    cursor = conn.cursor()
    
    # Verificar estrutura da tabela
    print("📋 Estrutura da tabela car_images:")
    cursor.execute("PRAGMA table_info(car_images)")
    columns = cursor.fetchall()
    for col in columns:
        print(f"  - {col[1]} ({col[2]})")
    print()
    
    # Contar total de registos
    cursor.execute("SELECT COUNT(*) FROM car_images")
    total = cursor.fetchone()[0]
    print(f"📈 Total de registos: {total}\n")
    
    # Contar registos com fotos
    cursor.execute("SELECT COUNT(*) FROM car_images WHERE photo_url IS NOT NULL AND photo_url != ''")
    with_photos = cursor.fetchone()[0]
    print(f"🖼️  Registos com fotos: {with_photos}")
    print(f"❌ Registos sem fotos: {total - with_photos}\n")
    
    # Mostrar alguns exemplos de URLs de fotos
    print("🔍 Exemplos de URLs de fotos guardadas:")
    cursor.execute("""
        SELECT model_key, photo_url, updated_at 
        FROM car_images 
        WHERE photo_url IS NOT NULL AND photo_url != ''
        LIMIT 10
    """)
    
    rows = cursor.fetchall()
    if rows:
        for row in rows:
            model_key, photo_url, updated_at = row
            print(f"  • {model_key}")
            print(f"    URL: {photo_url[:80]}...")
            print(f"    Atualizado: {updated_at}")
            print()
    else:
        print("  ⚠️  Nenhuma foto encontrada na base de dados!")
        print()
    
    # Verificar domínios das fotos
    print("🌐 Domínios das fotos:")
    cursor.execute("""
        SELECT DISTINCT 
            CASE 
                WHEN photo_url LIKE 'https://www.carjet.com/%' THEN 'carjet.com'
                WHEN photo_url LIKE 'https://cdn.%' THEN 'CDN'
                ELSE 'Outro'
            END as domain,
            COUNT(*) as count
        FROM car_images 
        WHERE photo_url IS NOT NULL AND photo_url != ''
        GROUP BY domain
    """)
    
    domains = cursor.fetchall()
    for domain, count in domains:
        print(f"  • {domain}: {count} fotos")
    print()
    
    # Listar todos os modelos
    print("📝 Todos os modelos na base de dados:")
    cursor.execute("SELECT model_key FROM car_images ORDER BY model_key")
    all_models = cursor.fetchall()
    for i, (model,) in enumerate(all_models, 1):
        print(f"  {i:3d}. {model}")
    
    conn.close()
    
    print("\n" + "="*60)
    print("✅ Diagnóstico completo!")
    print("="*60)

if __name__ == "__main__":
    main()
