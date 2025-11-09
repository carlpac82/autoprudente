#!/usr/bin/env python3
import requests
import sqlite3
import json

# Baixar coordenadas do Render
print("📥 Baixando coordenadas do Render...")
response = requests.get('https://carrental-api-5f8q.onrender.com/api/damage-reports/download-coordinates')

if response.status_code == 200:
    coords = response.json()
    print(f"✅ Recebidas {len(coords)} coordenadas do Render")
    
    # Conectar ao SQLite
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    
    # NÃO apagar! Só atualizar/inserir
    count_updated = 0
    count_inserted = 0
    
    for field_id, data in coords.items():
        # Verificar se existe
        cursor.execute("SELECT field_id FROM damage_report_coordinates WHERE field_id = ?", (field_id,))
        exists = cursor.fetchone()
        
        if exists:
            # Update
            cursor.execute("""
                UPDATE damage_report_coordinates 
                SET x = ?, y = ?, width = ?, height = ?, page = ?
                WHERE field_id = ?
            """, (data['x'], data['y'], data['width'], data['height'], data.get('page', 1), field_id))
            count_updated += 1
        else:
            # Insert
            cursor.execute("""
                INSERT INTO damage_report_coordinates (field_id, x, y, width, height, page)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (field_id, data['x'], data['y'], data['width'], data['height'], data.get('page', 1)))
            count_inserted += 1
        
        print(f"  {'📝' if exists else '➕'} {field_id}")
    
    conn.commit()
    conn.close()
    
    print(f"\n🎉 Restauração completa!")
    print(f"   📝 Atualizados: {count_updated}")
    print(f"   ➕ Inseridos: {count_inserted}")
    print(f"   📊 Total: {count_updated + count_inserted}")
else:
    print(f"❌ Erro ao baixar: HTTP {response.status_code}")
    print("Tentando método alternativo...")
