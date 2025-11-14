#!/usr/bin/env python3
"""
Testar fluxo completo: scraping → normalize_and_sort → frontend
"""
import sys
sys.path.insert(0, '/Users/filipepacheco/CascadeProjects/RentalPriceTrackerPerDay')

from carjet_direct import scrape_carjet_direct
from main import normalize_and_sort
from datetime import datetime, timedelta

print("="*100)
print("TESTE FLUXO COMPLETO - VW SHARAN")
print("="*100)

# 1. SCRAPING
start_dt = datetime(2025, 11, 19, 15, 0)
end_dt = start_dt + timedelta(days=5)

print("\n📥 PASSO 1: SCRAPING")
print("-"*100)
results = scrape_carjet_direct(
    location='Aeroporto de Faro',
    start_dt=start_dt,
    end_dt=end_dt
)

# Procurar VW Sharan
sharan_scraped = [r for r in results if 'sharan' in r.get('car', '').lower()]

if sharan_scraped:
    print(f"\n✅ {len(sharan_scraped)} VW Sharan encontrado no scraping:")
    for s in sharan_scraped:
        print(f"   Nome: {s.get('car')}")
        print(f"   Transmissão: {s.get('transmission')}")
        print(f"   Categoria: {s.get('category')}")
        print(f"   Supplier: {s.get('supplier')}")
        print(f"   Preço: {s.get('price')}")
else:
    print("\n❌ VW Sharan NÃO encontrado no scraping")
    sys.exit(1)

# 2. NORMALIZE_AND_SORT
print("\n\n📤 PASSO 2: NORMALIZE_AND_SORT")
print("-"*100)

normalized = normalize_and_sort(results, supplier_priority=None)

# Procurar VW Sharan no resultado normalizado
sharan_normalized = [r for r in normalized if 'sharan' in r.get('car', '').lower()]

if sharan_normalized:
    print(f"\n✅ {len(sharan_normalized)} VW Sharan encontrado após normalize:")
    for s in sharan_normalized:
        print(f"   Nome: {s.get('car')}")
        print(f"   Transmissão: {s.get('transmission')}")
        print(f"   Categoria: {s.get('category')}")
        print(f"   Grupo: {s.get('group')}")
        print(f"   Supplier: {s.get('supplier')}")
        print(f"   Preço: {s.get('price')}")
        print(f"   Tem ' Aut.' adicionado? {'aut.' in s.get('car', '').lower()}")
else:
    print("\n❌ VW Sharan NÃO encontrado após normalize")

# 3. COMPARAÇÃO
print("\n\n🔍 PASSO 3: COMPARAÇÃO")
print("-"*100)

if sharan_scraped and sharan_normalized:
    scraped = sharan_scraped[0]
    normalized_item = sharan_normalized[0]
    
    print(f"\nSCRAPING:")
    print(f"   Nome: {scraped.get('car')}")
    print(f"   Transmissão: {scraped.get('transmission')}")
    
    print(f"\nNORMALIZED:")
    print(f"   Nome: {normalized_item.get('car')}")
    print(f"   Transmissão: {normalized_item.get('transmission')}")
    print(f"   Grupo: {normalized_item.get('group')}")
    
    print(f"\nMUDANÇAS:")
    if scraped.get('car') != normalized_item.get('car'):
        print(f"   ⚠️  Nome mudou: '{scraped.get('car')}' → '{normalized_item.get('car')}'")
    if scraped.get('transmission') != normalized_item.get('transmission'):
        print(f"   ⚠️  Transmissão mudou: '{scraped.get('transmission')}' → '{normalized_item.get('transmission')}'")
    
    # Verificar problema
    trans = normalized_item.get('transmission', '').lower()
    grupo = normalized_item.get('group', '')
    has_aut = 'aut.' in normalized_item.get('car', '').lower()
    
    print(f"\nPROBLEMA?")
    if trans == 'manual' and grupo == 'M2':
        print(f"   ❌ SIM! Manual no grupo M2 (automático)")
    elif trans == 'automatic' and grupo == 'M1':
        print(f"   ❌ SIM! Automatic no grupo M1 (manual)")
    elif trans == 'manual' and has_aut:
        print(f"   ❌ SIM! Manual com ' Aut.' no nome")
    else:
        print(f"   ✅ Tudo correto")

print("\n" + "="*100)
