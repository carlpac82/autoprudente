#!/usr/bin/env python3
"""
Teste da API em produção - verifica se está retornando resultados
"""
import requests
import time
import sys

BASE_URL = "https://carrental-api-5f8q.onrender.com"

# Credenciais padrão (admin)
USERNAME = "admin"
PASSWORD = input("Digite a senha do admin: ").strip()

print(f"\n{'='*70}")
print(f"🧪 TESTE DA API EM PRODUÇÃO")
print(f"{'='*70}\n")

# Criar sessão
session = requests.Session()

# 1. LOGIN
print("1️⃣ Fazendo login...")
try:
    login_response = session.post(
        f"{BASE_URL}/login",
        data={"username": USERNAME, "password": PASSWORD},
        allow_redirects=True,
        timeout=10
    )
    
    if "/login" not in login_response.url and login_response.status_code == 200:
        print(f"   ✅ Login bem-sucedido!")
    else:
        print(f"   ❌ Login falhou! Status: {login_response.status_code}")
        print(f"   URL: {login_response.url}")
        sys.exit(1)
        
except Exception as e:
    print(f"   ❌ Erro no login: {e}")
    sys.exit(1)

# 2. TESTAR API DE PREÇOS
print(f"\n2️⃣ Testando API de preços...")
print(f"   Parâmetros:")
print(f"   - Location: Faro")
print(f"   - Dates: 2025-12-19 to 2026-01-02")
print(f"   - Time: 10:00")
print(f"\n   ⏱️  Aguardando resposta (isso pode demorar 20-60s)...\n")

params = {
    "location": "Faro",
    "start_date": "2025-12-19",
    "start_time": "10:00",
    "end_date": "2026-01-02",
    "end_time": "10:00"
}

start_time = time.time()

try:
    response = session.get(
        f"{BASE_URL}/api/prices",
        params=params,
        timeout=120  # 2 minutos de timeout
    )
    elapsed = time.time() - start_time
    
    print(f"\n{'='*70}")
    print(f"📊 RESULTADOS")
    print(f"{'='*70}\n")
    
    print(f"⏱️  Tempo de resposta: {elapsed:.2f}s")
    print(f"📡 Status HTTP: {response.status_code}")
    print(f"📦 Tamanho: {len(response.content):,} bytes")
    
    if response.status_code == 200:
        try:
            data = response.json()
            
            print(f"\n✅ Resposta JSON válida!")
            print(f"\n📋 Detalhes:")
            print(f"   - OK: {data.get('ok')}")
            print(f"   - Items: {len(data.get('items', []))}")
            print(f"   - Location: {data.get('location')}")
            print(f"   - Dates: {data.get('start_date')} to {data.get('end_date')}")
            print(f"   - Days: {data.get('days')}")
            
            if 'warning' in data:
                print(f"\n⚠️  Warning: {data['warning']}")
            
            items = data.get('items', [])
            if items:
                print(f"\n🚗 TOP 5 CARROS MAIS BARATOS:\n")
                for i, car in enumerate(items[:5], 1):
                    price = car.get('price', 'N/A')
                    name = car.get('name', 'N/A')
                    supplier = car.get('supplier', 'N/A')
                    group = car.get('group', 'N/A')
                    print(f"   {i}. €{price:>6} - {name} ({group})")
                    print(f"      Supplier: {supplier}")
                    
                print(f"\n✅ SUCESSO! API retornou {len(items)} carros")
            else:
                print(f"\n⚠️  ATENÇÃO! API retornou 0 carros")
                print(f"\n🔍 Resposta completa:")
                import json
                print(json.dumps(data, indent=2))
                
        except Exception as e:
            print(f"\n❌ Erro ao parsear JSON: {e}")
            print(f"\n📄 Conteúdo da resposta (primeiros 1000 chars):")
            print(response.text[:1000])
    else:
        print(f"\n❌ Status HTTP inválido: {response.status_code}")
        print(f"\n📄 Resposta:")
        print(response.text[:500])
    
except requests.Timeout:
    elapsed = time.time() - start_time
    print(f"\n❌ TIMEOUT após {elapsed:.2f}s")
    print(f"   A API não respondeu em 120 segundos")
    
except Exception as e:
    elapsed = time.time() - start_time
    print(f"\n❌ ERRO após {elapsed:.2f}s: {e}")

print(f"\n{'='*70}")

# Análise de performance
if elapsed < 30:
    print(f"✅ EXCELENTE! Tempo < 30s")
elif elapsed < 60:
    print(f"✅ BOM! Tempo < 60s")
else:
    print(f"⚠️  LENTO! Tempo > 60s (otimização necessária)")

print(f"{'='*70}\n")
