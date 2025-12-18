#!/usr/bin/env python3
"""
Teste direto do Selenium - chama a função internamente
"""

import os
import sys
from datetime import datetime

# Setar env vars ANTES de importar
os.environ['DISABLE_CARJET_REQUESTS'] = '1'
os.environ['USE_PLAYWRIGHT'] = 'false'

print("=" * 70)
print("TESTE DIRETO - SELENIUM APENAS (sem API web)")
print("=" * 70)
print(f"DISABLE_CARJET_REQUESTS={os.getenv('DISABLE_CARJET_REQUESTS')}")
print(f"USE_PLAYWRIGHT={os.getenv('USE_PLAYWRIGHT')}")
print("=" * 70)
print()

# Importar DEPOIS de setar env vars
sys.path.insert(0, os.path.dirname(__file__))

print("Importando módulos...")
from carjet_direct import scrape_carjet_with_selenium

# Parâmetros
location = "Albufeira"
start_dt = datetime(2025, 12, 21, 15, 0)
end_dt = datetime(2025, 12, 28, 15, 0)

print(f"📍 Location: {location}")
print(f"📅 Start: {start_dt.strftime('%d/%m/%Y %H:%M')}")
print(f"📅 End: {end_dt.strftime('%d/%m/%Y %H:%M')}")
print(f"⏳ Days: {(end_dt - start_dt).days}")
print()
print("🚀 Iniciando scraping com Selenium...")
print("=" * 70)
print()

try:
    results = scrape_carjet_with_selenium(location, start_dt, end_dt)
    
    print()
    print("=" * 70)
    print("RESULTADOS:")
    print("=" * 70)
    
    if results and len(results) > 0:
        print(f"✅ {len(results)} carros encontrados!")
        print()
        
        for i, car in enumerate(results[:5], 1):
            print(f"{i}. {car.get('supplier', 'N/A')} - {car.get('category', 'N/A')}")
            print(f"   💰 {car.get('price', 'N/A')} {car.get('currency', 'EUR')}")
            print(f"   🔗 {car.get('url', 'N/A')[:70]}...")
            print()
        
        if len(results) > 5:
            print(f"... e mais {len(results) - 5} carros")
    else:
        print("❌ Nenhum carro encontrado")
        print()
        print("⚠️  Possíveis causas:")
        print("   - Selenium não conseguiu submeter o formulário")
        print("   - Página de resultados não carregou")
        print("   - Parse HTML falhou")
        print("   - Site mudou estrutura")
    
    print()
    print("=" * 70)
    
except Exception as e:
    print()
    print("=" * 70)
    print("❌ ERRO:")
    print("=" * 70)
    print(f"{type(e).__name__}: {e}")
    print()
    import traceback
    traceback.print_exc()
