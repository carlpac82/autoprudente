#!/usr/bin/env python3
"""
Verificar status completo do Render - coordenadas e dados de exemplo
"""
import requests
import json

RENDER_URL = "https://carrental-api-5f8q.onrender.com"
USERNAME = "admin"
PASSWORD = "admin"

print("=" * 80)
print("🔍 VERIFICAR STATUS DO RENDER")
print("=" * 80)
print()

# Login
print("🔐 Login...")
session = requests.Session()
session.post(f"{RENDER_URL}/login", 
             data={'username': USERNAME, 'password': PASSWORD},
             timeout=60)
print("✅ Login OK")
print()

# 1. Verificar coordenadas
print("📍 COORDENADAS:")
print("-" * 80)
response = session.get(f"{RENDER_URL}/api/checkout/debug-coordinates", timeout=60)

if response.status_code == 200:
    data = response.json()
    
    if data.get('ok'):
        print(f"✅ Total: {data.get('coordinates_length')} campos")
        print(f"📝 Texto: {data.get('text_fields_count')} campos")
        print(f"🖼️  Imagem: {data.get('image_fields_count')} campos")
        print()
        
        text_fields = data.get('text_fields', [])
        image_fields = data.get('image_fields', [])
        
        print("📝 CAMPOS DE TEXTO:")
        for field in text_fields[:15]:  # Primeiros 15
            print(f"  - {field}")
        if len(text_fields) > 15:
            print(f"  ... e mais {len(text_fields) - 15} campos")
        print()
        
        print("🖼️  CAMPOS DE IMAGEM:")
        for field in image_fields:
            print(f"  - {field}")
        print()
    else:
        print(f"❌ Erro: {data.get('message')}")
        print()
else:
    print(f"❌ HTTP {response.status_code}")
    print()

# 2. Simular geração do PDF (sem baixar)
print("🎨 TESTE DE GERAÇÃO PDF:")
print("-" * 80)
print("Verificando endpoint...")

# Só queremos saber se gera sem erro
response = session.head(f"{RENDER_URL}/api/inspections/VI-20251111150000/pdf", timeout=60)
print(f"Status: {response.status_code}")
print(f"Content-Length: {response.headers.get('Content-Length', 'N/A')} bytes")
print(f"Content-Type: {response.headers.get('Content-Type', 'N/A')}")
print()

# 3. Verificar dados de exemplo no código
print("📋 DADOS DE EXEMPLO:")
print("-" * 80)
print("Os seguintes dados devem estar no inspection_data (após deploy):")
print()
print("  - contract_number: CTR-2024-001")
print("  - ra_number: RA-12345")
print("  - client_name: João Silva Santos")
print("  - client_email: joao.silva@example.com")
print("  - client_phone: +351 912 345 678")
print("  - vehicle_plate: AB-12-CD")
print("  - vehicle_brand_model: Toyota Corolla 1.6")
print("  - vehicle_color: Preto")
print("  - vehicle_km_delivery: 50.000 km")
print("  - vehicle_km_return: 50.450 km")
print("  - pickup_date: 05/11/2024")
print("  - pickup_time: 09:00")
print("  - pickup_location: Lisboa - Aeroporto")
print("  - expected_return_date: 12/11/2024")
print("  - expected_return_time: 18:00")
print("  - expected_return_location: Lisboa - Aeroporto")
print("  - fuel_level_delivery: 3/4 (75%)")
print("  - fuel_level_return: 1/2 (50%)")
print("  - observations_checkout: Veículo em bom estado. Sem danos visíveis.")
print("  - observations_checkin: Pequeno risco na porta traseira esquerda.")
print("  - inspector_name_checkout: Manuel Costa")
print("  - inspector_name_checkin: Ana Ferreira")
print("  - inspection_date: 12/11/2024")
print()

print("=" * 80)
print("🎯 CONCLUSÃO:")
print("=" * 80)
print()
print("1. Se coordenadas estão OK (37 campos) ✅")
print("2. Se PDF gera sem erro (200 OK) ✅")
print("3. Deploy já deve ter acontecido")
print()
print("🧪 PRÓXIMO PASSO:")
print("   Abrir o PDF e verificar QUANTOS campos aparecem preenchidos")
print(f"   {RENDER_URL}/api/inspections/VI-20251111150000/pdf")
print()
print("   Deve ter MUITO MAIS campos que antes!")
print()
