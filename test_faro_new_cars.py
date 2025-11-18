#!/usr/bin/env python3
"""
Pesquisar no Faro e verificar carros novos para adicionar ao VEHICLES
"""

import sys
from datetime import datetime, timedelta
from carjet_requests import scrape_carjet_requests
from carjet_direct import VEHICLES

# Pesquisa 1: 7 dias
location = "Faro"
start_dt = datetime.now() + timedelta(days=7)
end_dt = start_dt + timedelta(days=7)

print("=" * 80)
print(f"PESQUISA 1: Faro - 7 dias ({start_dt.strftime('%d/%m/%Y')} - {end_dt.strftime('%d/%m/%Y')})")
print("=" * 80)

try:
    results1 = scrape_carjet_requests(location, start_dt, end_dt)
    print(f"\n✅ Pesquisa 1: {len(results1)} carros encontrados")
except Exception as e:
    print(f"❌ Erro pesquisa 1: {e}")
    results1 = []

# Pesquisa 2: 30 dias
start_dt2 = datetime.now() + timedelta(days=30)
end_dt2 = start_dt2 + timedelta(days=7)

print("\n" + "=" * 80)
print(f"PESQUISA 2: Faro - 30 dias ({start_dt2.strftime('%d/%m/%Y')} - {end_dt2.strftime('%d/%m/%Y')})")
print("=" * 80)

try:
    results2 = scrape_carjet_requests(location, start_dt2, end_dt2)
    print(f"\n✅ Pesquisa 2: {len(results2)} carros encontrados")
except Exception as e:
    print(f"❌ Erro pesquisa 2: {e}")
    results2 = []

# Combinar resultados
all_results = results1 + results2
print(f"\n📊 Total combinado: {len(all_results)} carros")

# Verificar carros que NÃO estão no VEHICLES
cars_not_in_vehicles = {}
cars_in_vehicles = {}

for car_data in all_results:
    car_name = car_data.get('car', '').lower().strip()
    
    if not car_name:
        continue
    
    # Normalizar nome
    car_normalized = car_name.replace('.', '').replace(',', '')
    
    # Verificar se está no VEHICLES
    if car_normalized in VEHICLES:
        if car_normalized not in cars_in_vehicles:
            cars_in_vehicles[car_normalized] = {
                'original': car_data.get('car', ''),
                'category': VEHICLES[car_normalized],
                'group': car_data.get('group', ''),
                'transmission': car_data.get('transmission', ''),
                'count': 0
            }
        cars_in_vehicles[car_normalized]['count'] += 1
    else:
        if car_normalized not in cars_not_in_vehicles:
            cars_not_in_vehicles[car_normalized] = {
                'original': car_data.get('car', ''),
                'category': car_data.get('category', ''),
                'group': car_data.get('group', ''),
                'transmission': car_data.get('transmission', ''),
                'count': 0
            }
        cars_not_in_vehicles[car_normalized]['count'] += 1

print("\n" + "=" * 80)
print(f"📋 CARROS NO VEHICLES: {len(cars_in_vehicles)}")
print("=" * 80)
for car, data in sorted(cars_in_vehicles.items(), key=lambda x: x[1]['count'], reverse=True)[:10]:
    print(f"✅ {data['original']:40} | {data['category']:25} | {data['transmission']:10} | x{data['count']}")

print("\n" + "=" * 80)
print(f"🆕 CARROS NOVOS (NÃO NO VEHICLES): {len(cars_not_in_vehicles)}")
print("=" * 80)

if cars_not_in_vehicles:
    for car, data in sorted(cars_not_in_vehicles.items(), key=lambda x: x[1]['count'], reverse=True):
        print(f"❓ {data['original']:40} | {data['category']:25} | {data['group']:4} | {data['transmission']:10} | x{data['count']}")
    
    print("\n" + "=" * 80)
    print("💡 SUGESTÃO: Adicionar ao VEHICLES.py:")
    print("=" * 80)
    
    for car, data in sorted(cars_not_in_vehicles.items()):
        cat = data['category'] if data['category'] else 'VERIFICAR'
        print(f"    '{car}': '{cat}',  # {data['transmission']}")
else:
    print("✅ Todos os carros já estão no VEHICLES!")

print("\n" + "=" * 80)
print("RESUMO FINAL")
print("=" * 80)
print(f"Total carros encontrados: {len(all_results)}")
print(f"Carros no VEHICLES: {len(cars_in_vehicles)}")
print(f"Carros novos: {len(cars_not_in_vehicles)}")
print(f"Cobertura: {(len(cars_in_vehicles) / (len(cars_in_vehicles) + len(cars_not_in_vehicles)) * 100):.1f}%")
