#!/usr/bin/env python3
"""
Verificar tabelas no PostgreSQL do Render
"""

import requests

RENDER_URL = "https://carrental-api-9f8q.onrender.com"

# Testar se o endpoint temporário existe
print("🔍 A verificar endpoint temporário...")
response = requests.get(f"{RENDER_URL}/api/temp/upload-photo/test")
print(f"   Status: {response.status_code}")
print(f"   Response: {response.text[:200]}")
print()

# Testar endpoint de veículos
print("🔍 A verificar endpoint de veículos...")
response = requests.get(f"{RENDER_URL}/api/vehicles/with-originals")
print(f"   Status: {response.status_code}")
if response.status_code == 200:
    data = response.json()
    print(f"   OK: {data.get('ok')}")
    print(f"   Total veículos: {data.get('total')}")
    print(f"   Primeiros 3:")
    for i, (name, info) in enumerate(list(data.get('vehicles', {}).items())[:3]):
        print(f"      {i+1}. {name}")
else:
    print(f"   Erro: {response.text[:200]}")
