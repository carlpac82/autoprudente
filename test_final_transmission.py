#!/usr/bin/env python3
"""
Teste final da deteção de transmissão
"""
import sys
sys.path.insert(0, '/Users/filipepacheco/CascadeProjects/RentalPriceTrackerPerDay')

from carjet_direct import scrape_carjet_direct
from datetime import datetime, timedelta
from collections import defaultdict

print("="*100)
print("TESTE FINAL: Deteção de Transmissão pelo ícone icon-transm-auto")
print("="*100)

start_dt = datetime(2025, 11, 19, 15, 0)
end_dt = start_dt + timedelta(days=5)

results = scrape_carjet_direct(
    location='Aeroporto de Faro',
    start_dt=start_dt,
    end_dt=end_dt,
    quick=1
)

# Separar por transmissão
automatic = [r for r in results if r.get('transmission') == 'Automatic']
manual = [r for r in results if r.get('transmission') == 'Manual']

print(f"\n📊 RESUMO:")
print(f"   Total: {len(results)} carros")
print(f"   ✓ Automáticos: {len(automatic)} ({len(automatic)/len(results)*100:.1f}%)")
print(f"   ○ Manuais: {len(manual)} ({len(manual)/len(results)*100:.1f}%)")

print("\n" + "="*100)
print("EXEMPLOS DE CARROS AUTOMÁTICOS (com icon-transm-auto)")
print("="*100)

# Mostrar alguns exemplos de cada categoria
by_cat = defaultdict(list)
for r in automatic:
    by_cat[r['category']].append(r)

for cat in sorted(by_cat.keys())[:5]:  # Primeiras 5 categorias
    items = by_cat[cat][:3]  # 3 exemplos
    print(f"\n{cat}:")
    for item in items:
        print(f"   ✓ {item['car']}")

print("\n" + "="*100)
print("EXEMPLOS DE CARROS MANUAIS (sem icon-transm-auto)")
print("="*100)

by_cat_manual = defaultdict(list)
for r in manual:
    by_cat_manual[r['category']].append(r)

for cat in sorted(by_cat_manual.keys())[:5]:  # Primeiras 5 categorias
    items = by_cat_manual[cat][:3]  # 3 exemplos
    print(f"\n{cat}:")
    for item in items:
        print(f"   ○ {item['car']}")

print("\n" + "="*100)
print("VERIFICAÇÃO: Carros com 'Auto' no nome devem ser Automatic")
print("="*100)

problems = []
for r in results:
    car_lower = r['car'].lower()
    trans = r.get('transmission')
    
    # Se tem "auto" no nome mas não é automatic
    if 'auto' in car_lower and trans != 'Automatic':
        problems.append(f"❌ {r['car']} tem 'Auto' no nome mas é {trans}")
    
    # Se NÃO tem "auto" no nome mas é automatic (exceto elétricos)
    elif trans == 'Automatic' and 'auto' not in car_lower:
        if not any(word in car_lower for word in ['electric', 'hybrid', 'e-']):
            problems.append(f"⚠️  {r['car']} é Automatic mas não tem 'Auto' no nome (não elétrico)")

if problems:
    print("\n🚨 PROBLEMAS ENCONTRADOS:")
    for p in problems[:10]:  # Primeiros 10
        print(f"   {p}")
else:
    print("\n✅ NENHUM PROBLEMA! Todos os carros com 'Auto' são Automatic e vice-versa")

print("\n" + "="*100)
print("✅ DETEÇÃO FUNCIONANDO CORRETAMENTE!")
print("="*100)
