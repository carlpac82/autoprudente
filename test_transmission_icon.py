#!/usr/bin/env python3
"""
Teste de deteção de transmissão pelo ícone icon-transm-auto
"""
import sys
sys.path.insert(0, '/Users/filipepacheco/CascadeProjects/RentalPriceTrackerPerDay')

from carjet_direct import scrape_carjet_direct
from collections import defaultdict
from datetime import datetime, timedelta

print("Testando deteção de transmissão com ícone icon-transm-auto...")
print("="*100)

# Teste com Faro Airport
start_dt = datetime(2025, 11, 19, 15, 0)
end_dt = start_dt + timedelta(days=5)

results = scrape_carjet_direct(
    location='Aeroporto de Faro',
    start_dt=start_dt,
    end_dt=end_dt
)

print("\n" + "="*100)
print("RESULTADOS POR CATEGORIA")
print("="*100)

# Agrupar por categoria
by_cat = defaultdict(list)
for r in results:
    by_cat[r['category']].append(r)

# Mostrar carros de cada categoria
categories_order = [
    'MINI 4 Lugares',
    'MINI 5 Lugares', 
    'MINI Auto',
    'ECONOMY',
    'ECONOMY Auto',
    'Crossover',
    'SUV Auto',
    'SUV',
    'Cabrio',
    '7 Lugares',
    '7 Lugares Auto',
    '9 Lugares'
]

for cat in categories_order:
    if cat not in by_cat:
        continue
    
    items = by_cat[cat]
    print(f"\n{'='*100}")
    print(f"{cat} ({len(items)} carros)")
    print(f"{'='*100}")
    
    for item in items[:10]:  # Primeiros 10 de cada
        trans = item.get('transmission', 'N/A')
        icon = '✓' if trans == 'Automatic' else '○'
        price = float(item['price']) if isinstance(item['price'], (int, float)) else 0.0
        print(f"{icon} {item['car']:40} | Trans: {trans:10} | €{price:.2f}")

print("\n" + "="*100)
print("RESUMO")
print("="*100)

total = len(results)
automatic = sum(1 for r in results if r.get('transmission') == 'Automatic')
manual = sum(1 for r in results if r.get('transmission') == 'Manual')

print(f"Total: {total} carros")
print(f"Automáticos: {automatic} ({automatic/total*100:.1f}%)")
print(f"Manuais: {manual} ({manual/total*100:.1f}%)")
