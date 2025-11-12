#!/usr/bin/env python3
import os
import sys

# Importar as funções do main.py
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from main import _get_setting, _ensure_settings_table

# Garantir que a tabela existe
_ensure_settings_table()

# Buscar coordenadas
import json
coordinates_json = _get_setting('checkout_coordinates')

if coordinates_json:
    print(f"✅ Coordenadas encontradas!")
    print(f"📦 Raw JSON length: {len(coordinates_json)} chars")
    print(f"📦 First 300 chars: {coordinates_json[:300]}")
    print()
    
    # Parse
    coords = json.loads(coordinates_json)
    print(f"📊 Type: {type(coords).__name__}")
    print(f"📊 Length: {len(coords) if isinstance(coords, (list, dict)) else 'N/A'}")
    print()
    
    if isinstance(coords, list):
        print("📋 Array format (primeiros 3):")
        for i, item in enumerate(coords[:3]):
            print(f"  [{i}] {item}")
        print()
        
        # Verificar se tem field_id
        print("📝 Verificando field_ids:")
        field_ids = [item.get('field_id') for item in coords if isinstance(item, dict) and 'field_id' in item]
        print(f"  Total com field_id: {len(field_ids)}")
        print(f"  Primeiros 5: {field_ids[:5]}")
        
    elif isinstance(coords, dict):
        print("📋 Dict format (primeiros 3):")
        for key, value in list(coords.items())[:3]:
            print(f"  {key}: {value}")
    
else:
    print("❌ No coordinates found in settings!")
    print("⚠️  Verifica se salvaste no mapeador")
