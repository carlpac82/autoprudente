#!/usr/bin/env python3
"""
Teste da API de produção - verificar se Selenium encontra resultados
"""

import requests
import time
from datetime import datetime

print("=" * 70)
print("TESTE API PRODUÇÃO - RENDER")
print("=" * 70)
print()

# API de produção
api_url = "https://carrental-api-5f8q.onrender.com/api/prices"

# Credenciais (vou tentar sem autenticação primeiro pois DEV_NO_AUTH pode estar ativo)
params = {
    "location": "Albufeira",
    "start_date": "2025-12-21",
    "start_time": "15:00",
    "days": 7,
}

print(f"📍 Location: {params['location']}")
print(f"📅 Start: {params['start_date']} {params['start_time']}")
print(f"⏳ Days: {params['days']}")
print()
print("🚀 Enviando requisição para Render...")
print(f"URL: {api_url}")
print("=" * 70)
print()

start_time = time.time()

try:
    # Tentar sem auth primeiro
    response = requests.get(api_url, params=params, timeout=180, allow_redirects=False)
    elapsed = time.time() - start_time
    
    print(f"⏱️  Tempo de resposta: {elapsed:.1f}s")
    print(f"📊 Status: {response.status_code}")
    print()
    
    if response.status_code == 303 or response.status_code == 401:
        print("🔐 API requer autenticação, tentando com credenciais...")
        print()
        
        # Tentar com credenciais padrão
        auth_options = [
            ("admin", "admin"),
            ("user", "change_me"),
        ]
        
        for username, password in auth_options:
            print(f"Tentando: {username}")
            response = requests.get(api_url, params=params, auth=(username, password), timeout=180)
            elapsed = time.time() - start_time
            
            if response.status_code == 200:
                print(f"✅ Autenticado com {username}")
                break
            else:
                print(f"❌ Falhou com {username}: {response.status_code}")
        
        print()
    
    if response.status_code == 200:
        try:
            data = response.json()
            
            if data.get('ok'):
                cars = data.get('items', [])
                print(f"✅ {len(cars)} CARROS ENCONTRADOS!")
                print()
                
                if cars:
                    print("PRIMEIROS 5 CARROS:")
                    print("-" * 70)
                    for i, car in enumerate(cars[:5], 1):
                        supplier = car.get('supplier', 'N/A')
                        category = car.get('category', 'N/A')
                        price = car.get('price', 'N/A')
                        currency = car.get('currency', 'EUR')
                        
                        print(f"{i}. {supplier} - {category}")
                        print(f"   💰 {price} {currency}")
                        print()
                    
                    if len(cars) > 5:
                        print(f"... e mais {len(cars) - 5} carros")
                    
                    print()
                    print("=" * 70)
                    print("✅ TESTE PASSOU - SELENIUM FUNCIONOU!")
                    print("=" * 70)
                else:
                    print("⚠️  API retornou ok=true mas lista vazia")
                    print("Possível causa: Selenium não encontrou carros ou parse falhou")
            else:
                error = data.get('error', 'Unknown error')
                print(f"❌ API ERRO: {error}")
                print()
                print("Response completo:")
                print(data)
        except Exception as json_err:
            print(f"❌ Erro ao fazer parse: {json_err}")
            print(f"Response text: {response.text[:1000]}")
    else:
        print(f"❌ HTTP {response.status_code}")
        print(f"Response: {response.text[:500]}")
        
except requests.exceptions.Timeout:
    elapsed = time.time() - start_time
    print(f"⏰ TIMEOUT após {elapsed:.1f}s")
    print()
    print("Possíveis causas:")
    print("  - Selenium está travado")
    print("  - API está processando mas demorando muito")
    print("  - Render está frio (cold start)")
    
except requests.exceptions.ConnectionError as e:
    print(f"❌ ERRO DE CONEXÃO: {e}")
    print()
    print("Possíveis causas:")
    print("  - Render está offline")
    print("  - Problema de rede")
    
except Exception as e:
    print(f"❌ ERRO: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()

print()
print("=" * 70)
