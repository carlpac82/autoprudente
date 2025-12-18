#!/usr/bin/env python3
"""
Teste local da API com DISABLE_CARJET_REQUESTS=1
"""

import requests
import time
from datetime import datetime

print("=" * 70)
print("TESTE LOCAL - API COM SELENIUM APENAS")
print("=" * 70)
print()

# URL da API local
base_url = "http://localhost:8000"
api_url = f"{base_url}/api/prices"

# Autenticação (valores padrão do .env.example)
auth = ("user", "change_me")

# Parâmetros
params = {
    "location": "Albufeira",
    "start_date": "2025-12-21",
    "start_time": "15:00",
    "days": 7,
}

print(f"📍 Location: {params['location']}")
print(f"📅 Start: {params['start_date']} {params['start_time']}")
print(f"⏳ Days: {params['days']}")
print(f"🔐 Auth: {auth[0]}")
print()
print("🚀 Enviando requisição para API local...")
print(f"URL: {api_url}")
print(f"Params: {params}")
print("=" * 70)
print()

start_time = time.time()

try:
    response = requests.get(api_url, params=params, auth=auth, timeout=180)
    elapsed = time.time() - start_time
    
    print(f"⏱️  Tempo de resposta: {elapsed:.1f}s")
    print(f"📊 Status: {response.status_code}")
    print()
    
    if response.status_code == 200:
        # Debug: mostrar primeiros 500 chars da resposta
        print(f"Response content type: {response.headers.get('content-type')}")
        print(f"Response text (first 500 chars): {response.text[:500]}")
        print()
        
        try:
            data = response.json()
        except Exception as json_err:
            print(f"❌ Erro ao fazer parse do JSON: {json_err}")
            print(f"Response completo: {response.text[:2000]}")
            raise
        
        if data.get('ok'):
            cars = data.get('items', [])
            print(f"✅ {len(cars)} carros encontrados!")
            print()
            
            if cars:
                print("PRIMEIROS 5 CARROS:")
                print("-" * 70)
                for i, car in enumerate(cars[:5], 1):
                    print(f"{i}. {car.get('supplier', 'N/A')} - {car.get('category', 'N/A')}")
                    print(f"   💰 Preço: {car.get('price', 'N/A')} {car.get('currency', 'EUR')}")
                    print(f"   🔗 URL: {car.get('url', 'N/A')[:60]}...")
                    print()
                
                if len(cars) > 5:
                    print(f"... e mais {len(cars) - 5} carros")
            else:
                print("⚠️  Lista de carros vazia")
        else:
            error = data.get('error', 'Unknown error')
            print(f"❌ Erro na API: {error}")
    else:
        print(f"❌ HTTP {response.status_code}")
        print(f"Response: {response.text[:500]}")
        
except requests.exceptions.Timeout:
    elapsed = time.time() - start_time
    print(f"⏰ TIMEOUT após {elapsed:.1f}s")
    print("❌ A API demorou mais de 180s para responder")
    
except requests.exceptions.ConnectionError:
    print("❌ ERRO DE CONEXÃO")
    print("⚠️  Certifique-se que a API está rodando em http://localhost:5000")
    print()
    print("Para iniciar a API, execute:")
    print("  export DISABLE_CARJET_REQUESTS=1")
    print("  python3 main.py")
    
except Exception as e:
    print(f"❌ ERRO: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()

print()
print("=" * 70)
