#!/usr/bin/env python3
"""
Testa categorização de carros REAIS vindos do scraping
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from main import map_category_to_group, clean_car_name

# Simular carros que aparecem no scraping (124 carros sem categoria)
test_cars = [
    # Exemplos comuns que podem estar a falhar
    ("Fiat 500", "Mini 4 Seats"),
    ("Fiat 500 Auto", "Mini 4 Seats"),
    ("Peugeot 208", "Economy"),
    ("Peugeot 208 Auto", "Economy Automatic"),
    ("Toyota Chr", "SUV"),
    ("Toyota Chr Auto", "SUV Automatic"),
    ("Renault Clio", "Economy"),
    ("Renault Megane SW", "Station Wagon"),
    ("Opel Corsa", "Economy"),
    ("Nissan Qashqai", "SUV"),
    ("Volkswagen T-Roc", "SUV"),
    ("Seat Arona", "SUV"),
    ("Hyundai i10", "Mini 5 Seats"),
    ("Kia Picanto", "Mini 4 Seats"),
    ("Citroen C3", "Economy"),
    ("Dacia Sandero", "Economy"),
    ("Skoda Fabia", "Economy"),
    ("Ford Fiesta", "Economy"),
    ("Opel Astra", "Economy"),
    ("Volkswagen Golf", "Economy"),
    # Casos especiais
    ("", "Mini 4 Seats"),  # Sem nome de carro
    ("Unknown Car", ""),  # Sem categoria
    ("Fiat 500", ""),  # Sem categoria mas nome conhecido
]

print("=" * 80)
print("TESTE DE CATEGORIZAÇÃO - CARROS REAIS")
print("=" * 80)
print()

unmapped_count = 0
mapped_count = 0

for car_name, category in test_cars:
    group = map_category_to_group(category, car_name)
    
    # Verificar se ficou sem categoria
    is_unmapped = group == "Others" or not group
    
    if is_unmapped:
        unmapped_count += 1
        status = "❌ OTHERS"
        color = "\033[91m"  # Red
    else:
        mapped_count += 1
        status = f"✅ {group}"
        color = "\033[92m"  # Green
    
    reset = "\033[0m"
    
    print(f"{color}{status:15}{reset} | Car: {car_name:30} | Category: {category:25}")

print()
print("=" * 80)
print(f"RESUMO: {mapped_count} mapeados | {unmapped_count} sem categoria (Others)")
print("=" * 80)

# Testar normalização de nomes
print()
print("TESTE DE NORMALIZAÇÃO:")
print("-" * 80)
test_names = [
    "Fiat 500",
    "FIAT 500",
    "fiat 500",
    "Fiat 500 Auto",
    "Fiat 500 Automatic",
    "Fiat 500 Electric",
    "Peugeot 208 Hybrid",
    "Toyota Chr 4x4",
]

for name in test_names:
    clean = clean_car_name(name)
    print(f"Original: {name:30} → Clean: {clean}")
