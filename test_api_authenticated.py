#!/usr/bin/env python3
"""
Teste de performance da API com autenticação
"""
import requests
import time
import os

BASE_URL = "https://carrental-api-5f8q.onrender.com"
API_URL = f"{BASE_URL}/api/prices"

# Credenciais do .env
USERNAME = os.getenv("APP_USERNAME", "admin")
PASSWORD = os.getenv("APP_PASSWORD", "")

if not PASSWORD:
    print("⚠️ APP_PASSWORD não encontrado. Digite a senha:")
    PASSWORD = input().strip()

params = {
    "location": "Faro",
    "start_date": "2025-12-19",
    "start_time": "10:00",
    "end_date": "2026-01-02",
    "end_time": "10:00"
}

print(f"🧪 Testando API com autenticação...")
print(f"URL: {API_URL}")
print(f"User: {USERNAME}")
print(f"Parâmetros: {params}")
print(f"\n{'='*60}")

# Criar sessão para manter cookies
session = requests.Session()

# 1. Fazer login
print("\n1️⃣ Fazendo login...")
login_data = {
    "username": USERNAME,
    "password": PASSWORD
}

try:
    login_response = session.post(f"{BASE_URL}/login", data=login_data, allow_redirects=True)
    print(f"   Status: {login_response.status_code}")
    print(f"   URL final: {login_response.url}")
    
    if login_response.status_code == 200 and "/login" not in login_response.url:
        print("   ✅ Login bem-sucedido!")
    else:
        print("   ❌ Login falhou!")
        print(f"   Response: {login_response.text[:200]}")
        exit(1)
    
except Exception as e:
    print(f"   ❌ Erro no login: {e}")
    exit(1)

# 2. Testar API
print("\n2️⃣ Testando API de preços...")
print(f"   Aguardando resposta (timeout: 120s)...")

start_time = time.time()

try:
    response = session.get(API_URL, params=params, timeout=120)
    elapsed = time.time() - start_time
    
    print(f"\n✅ Resposta recebida em {elapsed:.2f}s")
    print(f"Status: {response.status_code}")
    print(f"Tamanho: {len(response.content)} bytes")
    
    # Verificar se é JSON
    content_type = response.headers.get('Content-Type', '')
    
    if response.status_code == 200 and 'application/json' in content_type:
        data = response.json()
        print(f"\n📊 Resultados:")
        print(f"   OK: {data.get('ok')}")
        print(f"   Items: {len(data.get('items', []))}")
        print(f"   Location: {data.get('location')}")
        print(f"   Dates: {data.get('start_date')} to {data.get('end_date')}")
        print(f"   Days: {data.get('days')}")
        
        if data.get('items'):
            print(f"\n🚗 Top 3 carros mais baratos:")
            for i, car in enumerate(data['items'][:3], 1):
                print(f"   {i}. {car.get('name')} - €{car.get('price')} - {car.get('supplier')} ({car.get('group', 'N/A')})")
        else:
            print("\n⚠️ Nenhum carro encontrado!")
            if 'warning' in data:
                print(f"   Warning: {data['warning']}")
    else:
        print(f"\n⚠️ Resposta inesperada")
        print(f"Content-Type: {content_type}")
        print(f"Body: {response.text[:500]}")
    
except requests.Timeout:
    elapsed = time.time() - start_time
    print(f"\n⏰ TIMEOUT após {elapsed:.2f}s")
    print(f"   A API demorou mais de 120 segundos para responder")
    
except Exception as e:
    elapsed = time.time() - start_time
    print(f"\n❌ Erro após {elapsed:.2f}s: {e}")

print(f"\n{'='*60}")
print(f"⏱️  Tempo total: {elapsed:.2f}s")

# Análise de performance
if elapsed < 30:
    print(f"✅ Excelente! Resposta em menos de 30s")
elif elapsed < 60:
    print(f"⚠️ Aceitável. Resposta em {elapsed:.2f}s (meta: <30s)")
else:
    print(f"❌ Lento! Resposta em {elapsed:.2f}s (meta: <30s)")
