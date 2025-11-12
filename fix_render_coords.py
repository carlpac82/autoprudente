#!/usr/bin/env python3
"""
Script para converter coordenadas no Render via API
"""
import requests
import json

RENDER_URL = "https://carrental-api-5f8q.onrender.com"
USERNAME = "admin"
PASSWORD = "admin"

# Lista de campos (mesma ordem do mapeador)
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
    'inspection_date'            # 39
]

print("=" * 80)
print("🔧 CONVERTER COORDENADAS NO RENDER")
print("=" * 80)
print()

# 1. Login
print("🔐 Fazendo login...")
session = requests.Session()
session.post(f"{RENDER_URL}/login", 
             data={'username': USERNAME, 'password': PASSWORD},
             timeout=60)
print("✅ Login OK")
print()

# 2. Buscar coordenadas atuais
print("📥 Buscando coordenadas do Render...")
response = session.get(f"{RENDER_URL}/api/checkout/debug-coordinates", timeout=60)

if response.status_code != 200:
    print(f"❌ Erro ao buscar: {response.status_code}")
    print(response.text)
    exit(1)

data = response.json()
print(f"📊 Status: {data}")
print()

if not data.get('has_coordinates'):
    print("❌ Nenhuma coordenada encontrada no Render!")
    exit(1)

# 3. Parse coordenadas
coords_type = data.get('coordinates_type')
first_items = data.get('first_items', [])

print(f"📋 Tipo: {coords_type}")
print(f"📋 Primeiros IDs: {first_items}")
print()

# Verificar se são numéricos
if all(str(item).isdigit() for item in first_items[:5]):
    print("⚠️  IDs são numéricos! Precisam ser convertidos.")
    print()
    
    # Fazer a conversão via script Python no Render seria complicado
    # Melhor: enviar coordenadas locais já convertidas!
    
    print("💡 SOLUÇÃO: Enviar coordenadas locais (já convertidas) para o Render")
    print()
    
    # Carregar coordenadas locais
    import sys
    import os
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from main import _get_setting
    
    coords_json = _get_setting('checkout_coordinates')
    if coords_json:
        coords = json.loads(coords_json)
        print(f"✅ Coordenadas locais carregadas: {len(coords)} campos")
        
        # Verificar se já estão convertidas
        sample_ids = [item.get('field_id') for item in coords[:3]]
        print(f"📝 Sample IDs locais: {sample_ids}")
        
        if not all(str(id).isdigit() for id in sample_ids):
            print("✅ Coordenadas locais já estão convertidas!")
            print()
            print("📤 Enviando para o Render...")
            
            response = session.post(
                f"{RENDER_URL}/api/checkout/save-coordinates",
                json=coords,
                timeout=60
            )
            
            result = response.json()
            print(f"📊 Resultado: {result}")
            
            if result.get('ok'):
                print()
                print("🎉 SUCESSO! Coordenadas enviadas para o Render!")
                print()
                print("🧪 Testa agora:")
                print(f"   {RENDER_URL}/api/inspections/VI-20251111150000/pdf")
            else:
                print(f"❌ Erro: {result.get('error')}")
        else:
            print("❌ Coordenadas locais também são numéricas!")
    else:
        print("❌ Nenhuma coordenada local encontrada!")
else:
    print("✅ IDs já estão em formato de nome! Não precisa converter.")
    print()
    print("🧪 Testa o PDF:")
    print(f"   {RENDER_URL}/api/inspections/VI-20251111150000/pdf")
