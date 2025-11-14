#!/usr/bin/env python3
"""
Testar carros específicos que o usuário diz estarem errados
"""
import sys
sys.path.insert(0, '/Users/filipepacheco/CascadeProjects/RentalPriceTrackerPerDay')

from carjet_direct import scrape_carjet_direct
from datetime import datetime, timedelta

print("="*100)
print("TESTE DE CARROS ESPECÍFICOS - Verificar transmissão")
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

# Carros específicos para testar
test_cars = [
    "ford galaxy",
    "ford kuga",
    "nissan juke",
    "opel zafira",
    "peugeot 308 sw auto",
    "volkswagen golf sw",
    "toyota yaris cross",
    "peugeot 5008",
    "opel mokka electric",
    "hyundai kona",
    "skoda octavia",
    "volkswagen taigo",
    "fiat talento",
    "renault megane sw",
]

print("="*100)
print("VERIFICAÇÃO DE CARROS ESPECÍFICOS")
print("="*100)
print(f"{'Carro':45} | {'Transmissão':15} | {'Tem Auto no nome?':20}")
print("-"*100)

for test_name in test_cars:
    # Procurar o carro nos resultados
    found = None
    for r in results:
        car = r.get('car', '').lower()
        if test_name in car:
            found = r
            break
    
    if found:
        car_name = found.get('car', '')
        trans = found.get('transmission', '')
        has_auto = 'auto' in car_name.lower()
        
        # Verificar se há problema
        problem = ''
        if has_auto and trans == 'Manual':
            problem = '❌ TEM AUTO MAS É MANUAL'
        elif not has_auto and trans == 'Automatic' and 'electric' not in car_name.lower() and 'hybrid' not in car_name.lower():
            problem = '⚠️  É AUTOMATIC MAS NÃO TEM AUTO'
        else:
            problem = '✅ OK'
        
        print(f"{problem} {car_name:45} | {trans:15} | {str(has_auto):20}")
    else:
        print(f"   {test_name:45} | NÃO ENCONTRADO")

print("\n" + "="*100)
