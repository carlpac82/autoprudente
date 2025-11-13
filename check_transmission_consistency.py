#!/usr/bin/env python3
"""
Verifica inconsistências na deteção de transmissão
"""
import sys
sys.path.insert(0, '/Users/filipepacheco/CascadeProjects/RentalPriceTrackerPerDay')

from carjet_direct import scrape_carjet_direct
from datetime import datetime, timedelta

print("Verificando inconsistências na deteção de transmissão...")
print("="*100)

# Teste com Faro Airport
start_dt = datetime(2025, 11, 19, 15, 0)
end_dt = start_dt + timedelta(days=5)

results = scrape_carjet_direct(
    location='Aeroporto de Faro',
    start_dt=start_dt,
    end_dt=end_dt,
    quick=1  # Quick mode para não fazer log excessivo
)

print("\n" + "="*100)
print("INCONSISTÊNCIAS ENCONTRADAS")
print("="*100)

inconsistencies = []

for r in results:
    car_name = r['car'].lower()
    trans = r.get('transmission', 'N/A')
    
    # Casos suspeitos: tem "auto" no nome mas é Manual
    if 'auto' in car_name and trans == 'Manual':
        inconsistencies.append({
            'car': r['car'],
            'trans': trans,
            'issue': 'Tem "Auto" no nome mas detectado como Manual'
        })
    
    # Casos suspeitos: NÃO tem "auto" no nome mas é Automatic
    # (exceto elétricos, híbridos que são sempre automáticos)
    elif trans == 'Automatic' and 'auto' not in car_name:
        if not any(word in car_name for word in ['electric', 'hybrid', 'híbrido', 'e-']):
            inconsistencies.append({
                'car': r['car'],
                'trans': trans,
                'issue': 'NÃO tem "Auto" no nome mas detectado como Automático (não é elétrico/híbrido)'
            })

if inconsistencies:
    print(f"\n⚠️  {len(inconsistencies)} INCONSISTÊNCIAS ENCONTRADAS:")
    print("-"*100)
    for inc in inconsistencies:
        print(f"• {inc['car']:50} | Trans: {inc['trans']:10} | {inc['issue']}")
else:
    print("\n✅ NENHUMA INCONSISTÊNCIA ENCONTRADA!")

print("\n" + "="*100)
print("VERIFICAÇÃO DE CARROS ESPECÍFICOS")
print("="*100)

# Carros que esperamos ser automáticos (do verify_all_groups.py)
expected_auto = [
    'Toyota Aygo Auto',
    'Fiat 500 Electric',
    'Renault Clio Auto',
    'Citroen C4 Electric',
    'Mercedes GLB 7 seater',
    'Ford Galaxy',
    'Ford Tourneo',
    'Volkswagen Multivan',
    'Mercedes V Class',
]

print("\nCarros que DEVEM ser automáticos:")
print("-"*100)

for expected in expected_auto:
    found = [r for r in results if expected.lower() in r['car'].lower()]
    if found:
        for r in found:
            trans = r.get('transmission', 'N/A')
            status = '✅' if trans == 'Automatic' else '❌'
            print(f"{status} {r['car']:45} | Trans: {trans}")
    else:
        print(f"⚠️  {expected:45} | NÃO ENCONTRADO")

print("\n" + "="*100)
