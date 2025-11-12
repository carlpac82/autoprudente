#!/usr/bin/env python3
"""
Script para converter field_ids numéricos para nomes corretos
"""
import os
import sys
import json

# Importar as funções do main.py
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from main import _get_setting, _set_setting, _ensure_settings_table

# Lista de campos na ordem correta (igual ao checkout_mapper_only.html)
FIELDS_TO_MAP = [
    'contract_number',           # 0
    'ra_number',                 # 1
    'contract_date',             # 2
    'client_name',               # 3
    'client_email',              # 4
    'client_phone',              # 5
    'client_address',            # 6
    'vehicle_plate',             # 7
    'vehicle_brand_model',       # 8
    'vehicle_color',             # 9
    'vehicle_km_delivery',       # 10
    'vehicle_km_return',         # 11
    'pickup_date',               # 12
    'pickup_time',               # 13
    'pickup_location',           # 14
    'expected_return_date',      # 15
    'expected_return_time',      # 16
    'expected_return_location',  # 17
    'fuel_level_delivery',       # 18
    'fuel_level_return',         # 19
    'photo_1_front',             # 20
    'photo_2_back',              # 21
    'photo_3_left',              # 22
    'photo_4_right',             # 23
    'photo_5',                   # 24
    'photo_6',                   # 25
    'photo_7',                   # 26
    'photo_8',                   # 27
    'photo_9',                   # 28
    'photo_10',                  # 29
    'diagram_checkout',          # 30
    'diagram_checkin',           # 31
    'observations_checkout',     # 32
    'observations_checkin',      # 33
    'inspector_name_checkout',   # 34
    'inspector_name_checkin',    # 35
    'inspector_signature_checkout', # 36
    'inspector_signature_checkin',  # 37
    'customer_signature',        # 38
    'inspection_date'            # 39 (não usado mas pode estar)
]

def main():
    print("=" * 80)
    print("🔧 CONVERTER FIELD_IDS NUMÉRICOS PARA NOMES")
    print("=" * 80)
    print()
    
    # Garantir que a tabela existe
    _ensure_settings_table()
    
    # Buscar coordenadas
    coordinates_json = _get_setting('checkout_coordinates')
    
    if not coordinates_json:
        print("❌ Nenhuma coordenada encontrada!")
        return
    
    # Parse coordenadas
    coords = json.loads(coordinates_json)
    
    if not isinstance(coords, list):
        print("❌ Coordenadas não estão em formato de array!")
        print(f"   Tipo: {type(coords)}")
        return
    
    print(f"📦 Encontradas {len(coords)} coordenadas")
    print()
    
    # Verificar se já estão corretas
    sample_ids = [item.get('field_id') for item in coords[:5] if isinstance(item, dict)]
    print(f"📝 Primeiros 5 IDs: {sample_ids}")
    print()
    
    # Verificar se são numéricos
    all_numeric = all(str(item.get('field_id', '')).isdigit() for item in coords if isinstance(item, dict))
    
    if not all_numeric:
        print("✅ Coordenadas já parecem estar corretas (não são numéricas)!")
        # Mostrar alguns exemplos
        print("\n📋 Exemplos:")
        for i, item in enumerate(coords[:3]):
            if isinstance(item, dict):
                print(f"  [{i}] field_id: '{item.get('field_id')}' at ({item.get('x')}, {item.get('y')}) page {item.get('page')}")
        return
    
    print("🔄 Convertendo IDs numéricos para nomes...")
    print()
    
    # Converter
    converted = []
    errors = []
    
    for item in coords:
        if not isinstance(item, dict):
            continue
        
        field_id_str = str(item.get('field_id', ''))
        
        if field_id_str.isdigit():
            index = int(field_id_str)
            
            if index < len(FIELDS_TO_MAP):
                new_field_id = FIELDS_TO_MAP[index]
                
                converted_item = {
                    'field_id': new_field_id,
                    'x': item.get('x'),
                    'y': item.get('y'),
                    'width': item.get('width'),
                    'height': item.get('height'),
                    'page': item.get('page', 1),
                    'field_type': item.get('field_type', 'text')
                }
                
                converted.append(converted_item)
                print(f"  ✓ [{index}] → '{new_field_id}' (page {item.get('page')})")
            else:
                errors.append(f"  ⚠️  Index {index} fora do range (máximo: {len(FIELDS_TO_MAP) - 1})")
        else:
            # Já não é numérico, manter como está
            converted.append(item)
            print(f"  ⊙ Mantido: '{field_id_str}'")
    
    print()
    print(f"✅ Convertidos: {len(converted)} campos")
    
    if errors:
        print(f"⚠️  Erros: {len(errors)}")
        for err in errors:
            print(err)
        print()
    
    # Mostrar exemplos da conversão
    print("📋 Exemplos convertidos:")
    for i, item in enumerate(converted[:5]):
        print(f"  [{i}] field_id: '{item.get('field_id')}' at ({item.get('x')}, {item.get('y')}) page {item.get('page')}")
    print()
    
    # Confirmar
    response = input("💾 Guardar as coordenadas convertidas? (s/n): ").strip().lower()
    
    if response == 's' or response == 'y':
        # Salvar
        _set_setting('checkout_coordinates', json.dumps(converted))
        print()
        print("✅ Coordenadas convertidas e salvas com sucesso!")
        print()
        print("🎉 Agora podes testar o PDF preview:")
        print("   http://localhost:8000/api/inspections/VI-20251111150000/pdf")
    else:
        print()
        print("❌ Conversão cancelada. Nenhuma alteração foi feita.")

if __name__ == '__main__':
    main()
