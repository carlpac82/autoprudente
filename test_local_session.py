#!/usr/bin/env python3
"""Teste local com sessão (login primeiro)"""

import requests
import time

session = requests.Session()
base_url = "http://localhost:8000"

print("=" * 70)
print("TESTE LOCAL - SELENIUM")
print("=" * 70)

# 1. Login
print("\n🔐 Fazendo login...")
login_resp = session.post(f"{base_url}/login", data={
    "username": "admin",
    "password": "admin"
}, allow_redirects=False)

print(f"Login status: {login_resp.status_code}")
if login_resp.status_code in [302, 303]:
    print("✅ Login OK - sessão criada")
else:
    print(f"❌ Login falhou: {login_resp.text[:200]}")
    exit(1)

# 2. Chamar API
print("\n🚀 Chamando API de preços...")
print("📍 Location: Albufeira")
print("📅 Data: 2025-12-21, 7 dias")
print("⏳ Aguarde (pode demorar 30-60s com Selenium)...")
print()

start = time.time()
try:
    resp = session.get(f"{base_url}/api/prices", params={
        "location": "Albufeira",
        "start_date": "2025-12-21",
        "start_time": "15:00",
        "days": 7
    }, timeout=180)
    
    elapsed = time.time() - start
    print(f"⏱️  Tempo: {elapsed:.1f}s")
    print(f"📊 Status: {resp.status_code}")
    
    if resp.status_code == 200:
        try:
            data = resp.json()
            if data.get('ok'):
                cars = data.get('items', [])
                print(f"\n✅ {len(cars)} CARROS ENCONTRADOS!")
                
                if cars:
                    print("\nPRIMEIROS 5:")
                    print("-" * 50)
                    for i, car in enumerate(cars[:5], 1):
                        print(f"{i}. {car.get('supplier')} - {car.get('category')}")
                        print(f"   💰 {car.get('price')} EUR")
                else:
                    print("⚠️  Lista vazia")
            else:
                print(f"❌ API erro: {data.get('error')}")
        except Exception as e:
            print(f"❌ JSON parse error: {e}")
            print(f"Response: {resp.text[:500]}")
    else:
        print(f"❌ HTTP {resp.status_code}")
        print(f"Response: {resp.text[:500]}")
        
except requests.exceptions.Timeout:
    print(f"⏰ TIMEOUT após {time.time()-start:.0f}s")
except Exception as e:
    print(f"❌ Erro: {e}")

print("\n" + "=" * 70)
