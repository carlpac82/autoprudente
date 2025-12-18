#!/usr/bin/env python3
"""
Teste local do Selenium com DISABLE_CARJET_REQUESTS=1
"""

import os
import sys
from datetime import datetime, timedelta

# Setar variável de ambiente ANTES de importar main
os.environ['DISABLE_CARJET_REQUESTS'] = '1'
os.environ['USE_PLAYWRIGHT'] = 'false'  # Garantir que Playwright não é usado

print("=" * 60)
print("TESTE LOCAL - SELENIUM APENAS")
print("=" * 60)
print(f"DISABLE_CARJET_REQUESTS={os.getenv('DISABLE_CARJET_REQUESTS')}")
print(f"USE_PLAYWRIGHT={os.getenv('USE_PLAYWRIGHT')}")
print("=" * 60)
print()

# Importar após setar env vars
from main import scrape_carjet

# Parâmetros de teste
location = "Albufeira"
start_dt = datetime(2025, 12, 21, 15, 0)
end_dt = datetime(2025, 12, 28, 15, 0)

print(f"📍 Location: {location}")
print(f"📅 Start: {start_dt}")
print(f"📅 End: {end_dt}")
print(f"⏳ Days: {(end_dt - start_dt).days}")
print()
print("🚀 Iniciando scraping...")
print("=" * 60)
print()

try:
    results = scrape_carjet(location, start_dt, end_dt)
    
    print()
    print("=" * 60)
    print("RESULTADOS:")
    print("=" * 60)
    
    if results:
        print(f"✅ {len(results)} carros encontrados!")
        print()
        for i, car in enumerate(results[:5], 1):
            print(f"{i}. {car.get('supplier', 'N/A')} - {car.get('category', 'N/A')}")
            print(f"   Preço: {car.get('price', 'N/A')} {car.get('currency', 'EUR')}")
            print(f"   URL: {car.get('url', 'N/A')[:80]}...")
            print()
        
        if len(results) > 5:
            print(f"... e mais {len(results) - 5} carros")
    else:
        print("❌ Nenhum carro encontrado")
        print("⚠️  Verifique os logs acima para identificar o problema")
    
except Exception as e:
    print()
    print("=" * 60)
    print("❌ ERRO:")
    print("=" * 60)
    print(f"{type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
