#!/usr/bin/env python3
"""
Copiar coordenadas mapeadas do Render (PostgreSQL) para SQLite local
"""

import requests
import sqlite3
import json
from datetime import datetime

RENDER_URL = "https://carrental-api-5f8q.onrender.com"

def sync_coordinates():
    print("\n🔄 SINCRONIZAR COORDENADAS DO RENDER\n")
    print("=" * 60)
    
    # 1. Buscar coordenadas do Render
    print("\n📥 Buscando coordenadas do Render...")
    try:
        response = requests.get(f"{RENDER_URL}/api/damage-reports/get-coordinates-public")
        response.raise_for_status()
        data = response.json()
        
        if not data.get('ok'):
            print(f"❌ Erro: {data.get('error', 'Unknown error')}")
            return
        
        coordinates = data.get('coordinates', {})
        print(f"✅ Encontradas {len(coordinates)} coordenadas no Render")
        
        if len(coordinates) == 0:
            print("\n⚠️  Nenhuma coordenada encontrada no Render!")
            print("Verifica se fizeste login e se as coordenadas foram guardadas.")
            return
            
    except Exception as e:
        print(f"❌ Erro ao buscar do Render: {e}")
        return
    
    # 2. Guardar no SQLite local
    print("\n💾 Guardando no SQLite local...")
    try:
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        
        # Limpar coordenadas antigas
        cursor.execute("DELETE FROM damage_report_coordinates")
        cursor.execute("DELETE FROM damage_report_mapping_history")
        print("   Coordenadas antigas removidas")
        
        # Inserir novas
        count = 0
        for field_id, coord in coordinates.items():
            # Detectar tipo de campo
            field_type = 'text'
            if 'photo' in field_id or 'diagram' in field_id or 'signature' in field_id:
                field_type = 'image'
            elif 'repair' in field_id and 'line' in field_id:
                field_type = 'table'
            
            # Inserir coordenada
            cursor.execute("""
                INSERT INTO damage_report_coordinates 
                (field_id, x, y, width, height, page, field_type, template_version, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                field_id,
                coord['x'],
                coord['y'],
                coord['width'],
                coord['height'],
                coord.get('page', 1),
                field_type,
                1,  # template_version
                datetime.now().isoformat()
            ))
            
            # Inserir histórico
            cursor.execute("""
                INSERT INTO damage_report_mapping_history 
                (template_version, field_id, x, y, width, height, page, field_type, mapped_by, mapped_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                1,  # template_version
                field_id,
                coord['x'],
                coord['y'],
                coord['width'],
                coord['height'],
                coord.get('page', 1),
                field_type,
                'sync_script',
                datetime.now().isoformat()
            ))
            count += 1
        
        conn.commit()
        conn.close()
        
        print(f"✅ {count} coordenadas guardadas no SQLite local")
        
    except Exception as e:
        print(f"❌ Erro ao guardar no SQLite: {e}")
        return
    
    # 3. Guardar backup JSON
    print("\n📄 Guardando backup JSON...")
    try:
        with open('damage_report_coordinates.json', 'w') as f:
            json.dump(coordinates, f, indent=2)
        print("✅ Backup JSON criado")
    except Exception as e:
        print(f"⚠️  Erro ao criar backup JSON: {e}")
    
    # 4. Mostrar resumo
    print("\n" + "=" * 60)
    print("\n📊 RESUMO:")
    
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    
    # Total
    cursor.execute("SELECT COUNT(*) FROM damage_report_coordinates")
    total = cursor.fetchone()[0]
    print(f"   Total de campos: {total}")
    
    # Por tipo
    types = [
        ('Danos (damage_description_line_*)', "field_id LIKE 'damage_description_line_%'"),
        ('Reparação (repair_line_*)', "field_id LIKE 'repair_line%'"),
        ('Fotos (damage_photo_*)', "field_id LIKE 'damage_photo_%'"),
        ('Diagrama (vehicle_diagram)', "field_id = 'vehicle_diagram'"),
        ('Assinaturas (signature_*)', "field_id LIKE 'signature_%'"),
    ]
    
    for name, condition in types:
        cursor.execute(f"SELECT COUNT(*) FROM damage_report_coordinates WHERE {condition}")
        count = cursor.fetchone()[0]
        if count > 0:
            print(f"   - {name}: {count}")
    
    conn.close()
    
    print("\n✅ Sincronização completa!")
    print("\nAgora podes testar o preview localmente.")
    print("=" * 60 + "\n")

if __name__ == "__main__":
    sync_coordinates()
