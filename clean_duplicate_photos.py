#!/usr/bin/env python3
"""
Remove fotos duplicadas (genéricas) do car_images.db
Mantém apenas fotos únicas para cada carro
"""

import sqlite3
from pathlib import Path

def main():
    db_path = Path(__file__).parent / "car_images.db"
    
    if not db_path.exists():
        print(f"❌ {db_path} não encontrado")
        return
    
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    
    # Encontrar fotos duplicadas (usadas por mais de 3 carros)
    print("🔍 Procurando fotos duplicadas...")
    duplicates = cursor.execute("""
        SELECT photo_url, COUNT(*) as count, GROUP_CONCAT(model_key, ', ') as cars
        FROM car_images 
        WHERE photo_url NOT LIKE '%loading-car%'
        GROUP BY photo_url 
        HAVING count > 3
        ORDER BY count DESC
    """).fetchall()
    
    print(f"\n📊 Encontradas {len(duplicates)} fotos duplicadas:")
    print("="*80)
    
    total_removed = 0
    
    for photo_url, count, cars in duplicates:
        print(f"\n🖼️  {photo_url}")
        print(f"   Usada por {count} carros: {cars[:100]}...")
        
        # Perguntar se deve remover
        response = input(f"   Remover esta foto de TODOS os carros? (y/N): ").strip().lower()
        
        if response == 'y':
            # Marcar como placeholder
            cursor.execute("""
                UPDATE car_images 
                SET photo_url = 'https://www.carjet.com/cdn/img/cars/loading-car.png'
                WHERE photo_url = ?
            """, (photo_url,))
            
            conn.commit()
            total_removed += count
            print(f"   ✅ Removida de {count} carros")
        else:
            print(f"   ⏭️  Mantida")
    
    conn.close()
    
    print("\n" + "="*80)
    print(f"✅ Total de fotos removidas: {total_removed}")
    print("="*80)
    
    print("\n💡 Próximo passo: Execute novamente o scraper para obter fotos específicas")

if __name__ == "__main__":
    main()
