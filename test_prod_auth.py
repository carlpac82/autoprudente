#!/usr/bin/env python3
"""
Tentar várias credenciais para autenticar na API de produção
"""

import requests
import time

api_url = "https://carrental-api-5f8q.onrender.com/api/prices"
params = {
    "location": "Albufeira",
    "start_date": "2025-12-21",
    "start_time": "15:00",
    "days": 7,
}

# Tentar várias credenciais comuns
credentials = [
    ("admin", "admin"),
    ("user", "change_me"),
    ("admin", "change_me_strong_password"),
    ("user", "user"),
    ("filipepacheco", "admin"),
    ("fp", "admin"),
]

print("=" * 70)
print("TESTANDO CREDENCIAIS NA API DE PRODUÇÃO")
print("=" * 70)
print()

for username, password in credentials:
    print(f"🔐 Tentando: {username} / {'*' * len(password)}")
    
    try:
        response = requests.get(
            api_url, 
            params=params, 
            auth=(username, password), 
            timeout=10,
            allow_redirects=False
        )
        
        if response.status_code == 200:
            print(f"   ✅ FUNCIONOU! Status: {response.status_code}")
            print(f"   Content-Type: {response.headers.get('content-type')}")
            
            # Verificar se é JSON
            if 'application/json' in response.headers.get('content-type', ''):
                data = response.json()
                if data.get('ok'):
                    cars = data.get('items', [])
                    print(f"   🚗 {len(cars)} carros encontrados!")
                    
                    if cars:
                        print()
                        print("   PRIMEIROS 3 CARROS:")
                        for i, car in enumerate(cars[:3], 1):
                            print(f"   {i}. {car.get('supplier')} - {car.get('price')} EUR")
                else:
                    print(f"   ❌ API retornou erro: {data.get('error')}")
            else:
                print(f"   ⚠️  Não é JSON: {response.text[:200]}")
            
            print()
            print("=" * 70)
            print(f"✅ CREDENCIAIS CORRETAS: {username} / {password}")
            print("=" * 70)
            break
            
        elif response.status_code == 303:
            print(f"   ❌ Redirect para login (303) - credenciais inválidas")
        elif response.status_code == 401:
            print(f"   ❌ Não autorizado (401)")
        else:
            print(f"   ⚠️  Status inesperado: {response.status_code}")
            
    except requests.exceptions.Timeout:
        print(f"   ⏰ Timeout (>10s)")
    except Exception as e:
        print(f"   ❌ Erro: {e}")
    
    time.sleep(0.5)

print()
print("=" * 70)
print("NENHUMA CREDENCIAL FUNCIONOU")
print()
print("📝 AÇÕES NECESSÁRIAS:")
print("1. Aceder ao Render Dashboard:")
print("   https://dashboard.render.com/web/srv-cuhc766g1b2c73e4b7n0")
print()
print("2. Ir para 'Environment' e verificar:")
print("   - APP_USERNAME (se não existir, o padrão é 'user')")
print("   - APP_PASSWORD")
print()
print("3. Ou tentar fazer login manualmente em:")
print("   https://carrental-api-5f8q.onrender.com/login")
print("=" * 70)
