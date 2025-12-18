#!/usr/bin/env python3
"""
Teste de performance da API - mede tempo de resposta
"""
import requests
import time
import json

API_URL = "https://carrental-api-5f8q.onrender.com/api/prices"

params = {
    "location": "Faro",
    "start_date": "2025-12-19",
    "start_time": "10:00",
    "end_date": "2026-01-02",
    "end_time": "10:00"
}

print(f"🧪 Testando API...")
print(f"URL: {API_URL}")
print(f"Parâmetros: {params}")
print(f"\n{'='*60}")

# Criar sessão para manter cookies
session = requests.Session()

# 1. Fazer login primeiro (se necessário)
print("\n1️⃣ Verificando acesso...")
start_time = time.time()

try:
    response = session.get(API_URL, params=params, timeout=120, allow_redirects=True)
    elapsed = time.time() - start_time
    
    print(f"\n✅ Resposta recebida em {elapsed:.2f}s")
    print(f"Status: {response.status_code}")
    print(f"URL final: {response.url}")
    print(f"Tamanho: {len(response.content)} bytes")
    
    # Verificar se é HTML (redirect para login) ou JSON
    content_type = response.headers.get('Content-Type', '')
    
    if 'application/json' in content_type:
        data = response.json()
        print(f"\n📊 Resultados:")
        print(f"   OK: {data.get('ok')}")
        print(f"   Items: {len(data.get('items', []))}")
        
        if data.get('items'):
            print(f"\n🚗 Primeiro carro:")
            first = data['items'][0]
            print(f"   Nome: {first.get('name')}")
            print(f"   Preço: €{first.get('price')}")
            print(f"   Fornecedor: {first.get('supplier')}")
            print(f"   Grupo: {first.get('group')}")
    else:
        print(f"\n⚠️ Resposta não é JSON (provavelmente redirect para login)")
        print(f"Content-Type: {content_type}")
        if 'text/html' in content_type:
            print("📄 Recebeu página HTML (login necessário)")
    
except requests.Timeout:
    elapsed = time.time() - start_time
    print(f"\n⏰ TIMEOUT após {elapsed:.2f}s")
    
except Exception as e:
    elapsed = time.time() - start_time
    print(f"\n❌ Erro após {elapsed:.2f}s: {e}")

print(f"\n{'='*60}")
print(f"⏱️  Tempo total: {elapsed:.2f}s")
print(f"\n💡 Nota: Se recebeu redirect para login, a API requer autenticação")
print(f"   Acesse https://carrental-api-5f8q.onrender.com no browser primeiro")
