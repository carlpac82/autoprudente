#!/usr/bin/env python3
"""
Testar especificamente o Volkswagen Sharan
"""
import sys
sys.path.insert(0, '/Users/filipepacheco/CascadeProjects/RentalPriceTrackerPerDay')

from carjet_direct import scrape_carjet_direct
from datetime import datetime, timedelta

print("="*100)
print("TESTE: VOLKSWAGEN SHARAN")
print("="*100)

# Fazer scraping
start_dt = datetime(2025, 11, 19, 15, 0)
end_dt = start_dt + timedelta(days=5)

print("\n🔍 Fazendo scraping...")
results = scrape_carjet_direct(
    location='Aeroporto de Faro',
    start_dt=start_dt,
    end_dt=end_dt
)

print(f"✅ {len(results)} carros encontrados\n")

# Procurar Volkswagen Sharan
print("="*100)
print("VOLKSWAGEN SHARAN - DETALHES COMPLETOS")
print("="*100)

for r in results:
    car = r.get('car', '')
    if 'sharan' in car.lower():
        print(f"\nCarro: {car}")
        print(f"Transmissão: {r.get('transmission', 'N/A')}")
        print(f"Categoria: {r.get('category', 'N/A')}")
        print(f"Supplier: {r.get('supplier', 'N/A')}")
        print(f"Preço: {r.get('price', 'N/A')}")
        print(f"Tem 'Auto' no nome? {'auto' in car.lower()}")
        print(f"Tem 'icon-transm-auto' no HTML? (verificado no scraping)")
        print("-"*100)

print("\n" + "="*100)
print("ANÁLISE")
print("="*100)

sharan_found = [r for r in results if 'sharan' in r.get('car', '').lower()]

if sharan_found:
    print(f"\n✅ {len(sharan_found)} Volkswagen Sharan encontrado(s)")
    
    for idx, s in enumerate(sharan_found, 1):
        car = s.get('car', '')
        trans = s.get('transmission', '')
        has_auto = 'auto' in car.lower()
        
        print(f"\n{idx}. {car}")
        print(f"   Transmissão: {trans}")
        print(f"   Tem 'Auto' no nome: {has_auto}")
        
        # Verificar qual grupo deveria ir
        if has_auto or trans == 'Automatic':
            print(f"   ✅ Grupo esperado: M2 (7 Seater Auto)")
        else:
            print(f"   ✅ Grupo esperado: M1 (7 Seater Manual)")
        
        # Verificar problema
        if not has_auto and trans == 'Automatic':
            print(f"   ❌ PROBLEMA: É Automatic mas não tem 'Auto' no nome!")
        elif has_auto and trans == 'Manual':
            print(f"   ❌ PROBLEMA: Tem 'Auto' no nome mas é Manual!")
else:
    print("\n❌ Volkswagen Sharan NÃO encontrado")

print("\n" + "="*100)
