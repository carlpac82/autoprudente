#!/usr/bin/env python3
"""
Teste ao vivo da deteção de transmissão
"""
import sys
sys.path.insert(0, '/Users/filipepacheco/CascadeProjects/RentalPriceTrackerPerDay')

from carjet_direct import scrape_carjet_direct
from datetime import datetime, timedelta

print("="*100)
print("TESTE AO VIVO - Deteção de Transmissão")
print("="*100)

# Fazer scraping real
start_dt = datetime(2025, 11, 19, 15, 0)
end_dt = start_dt + timedelta(days=5)

print("\nFazendo scraping real da CarJet...")
results = scrape_carjet_direct(
    location='Aeroporto de Faro',
    start_dt=start_dt,
    end_dt=end_dt
)

print(f"\n✅ {len(results)} carros encontrados\n")

# Mostrar primeiros 30 com detalhes
print("="*100)
print("PRIMEIROS 30 CARROS - Verificar se deteção está correta")
print("="*100)
print(f"{'Carro':45} | {'Transmissão':12} | {'Categoria':25}")
print("-"*100)

for r in results[:30]:
    car = r.get('car', 'N/A')
    trans = r.get('transmission', 'N/A')
    cat = r.get('category', 'N/A')
    
    # Highlight potential issues
    car_lower = car.lower()
    has_auto_in_name = 'auto' in car_lower
    is_electric = any(w in car_lower for w in ['electric', 'hybrid', 'e-'])
    
    marker = ''
    if has_auto_in_name and trans == 'Manual':
        marker = '❌ '  # Tem Auto no nome mas é Manual
    elif not has_auto_in_name and not is_electric and trans == 'Automatic':
        marker = '⚠️  '  # É Automatic mas não tem Auto no nome (não elétrico)
    else:
        marker = '✅ '
    
    print(f"{marker}{car:45} | {trans:12} | {cat:25}")

print("\n" + "="*100)
print("RESUMO")
print("="*100)

auto_count = sum(1 for r in results if r.get('transmission') == 'Automatic')
manual_count = sum(1 for r in results if r.get('transmission') == 'Manual')
total = len(results)

print(f"Total: {total}")
print(f"Automáticos: {auto_count} ({auto_count/total*100:.1f}%)")
print(f"Manuais: {manual_count} ({manual_count/total*100:.1f}%)")

# Procurar casos específicos problemáticos
print("\n" + "="*100)
print("CASOS PROBLEMÁTICOS")
print("="*100)

problems = []
for r in results:
    car = r.get('car', '')
    trans = r.get('transmission', '')
    car_lower = car.lower()
    
    # Caso 1: Tem "auto" no nome mas é Manual
    if 'auto' in car_lower and trans == 'Manual':
        problems.append(f"❌ {car} → Tem 'Auto' no nome mas é MANUAL")
    
    # Caso 2: Não tem "auto", não é elétrico, mas é Automatic
    elif trans == 'Automatic' and 'auto' not in car_lower:
        if not any(w in car_lower for w in ['electric', 'hybrid', 'e-']):
            problems.append(f"⚠️  {car} → É AUTOMATIC mas não tem 'Auto' no nome (não é elétrico)")

if problems:
    print(f"\n⚠️  {len(problems)} PROBLEMAS ENCONTRADOS:\n")
    for p in problems[:20]:  # Primeiros 20
        print(f"   {p}")
else:
    print("\n✅ NENHUM PROBLEMA ENCONTRADO!")

print("\n" + "="*100)
