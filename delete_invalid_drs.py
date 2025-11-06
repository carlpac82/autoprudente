#!/usr/bin/env python3
"""Script para eliminar DRs com formato inválido via API"""
import requests

# URL da API
API_URL = "https://carrental-api.onrender.com/api/damage-reports/cleanup-invalid"

print("🔄 A eliminar DRs inválidos (1:2025, 2:2025, 3:2025)...")

try:
    response = requests.post(API_URL)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text[:200]}")
    
    result = response.json()
    
    if result.get("ok"):
        print(f"\n✅ {result.get('message', 'Sucesso')}")
        if result.get("deleted"):
            print(f"   Eliminados: {', '.join(result['deleted'])}")
        if result.get("errors"):
            print(f"   Erros: {', '.join(result['errors'])}")
    else:
        print(f"❌ Erro: {result.get('error', 'Desconhecido')}")
        
except Exception as e:
    print(f"❌ Erro: {e}")
