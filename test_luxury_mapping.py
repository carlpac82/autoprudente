#!/usr/bin/env python3
"""
Testa mapeamento de carros Luxury - devem ir para Others
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from main import map_category_to_group

# Carros Luxury que devem ir para Others
luxury_cars = [
    ("Mini Cooper", "Luxury"),
    ("Mini Countryman", "Luxury"),
    ("BMW 1 Series Auto", "Luxury"),
    ("Mercedes A Class Auto", "Luxury"),
    ("Audi A3 Auto", "Luxury"),
    ("Mercedes GLA Auto", "Luxury"),
    ("Cupra Formentor", "Luxury"),
    ("Range Rover Evoque", "Luxury"),
    ("Porsche Cayenne Auto", "Luxury"),
    ("Volvo XC90 Auto", "Luxury"),
]

# Carros Cabrio que devem ir para G
cabrio_cars = [
    ("Fiat 500 Cabrio", "Cabrio"),
    ("Mini Cooper Cabrio", "Cabrio"),
    ("VW Beetle Cabrio", "Cabrio"),
    ("BMW 4 Series Cabrio Auto", "Cabrio"),
    ("Mazda MX5 Cabrio Auto", "Cabrio"),
]

print("=" * 80)
print("TESTE DE MAPEAMENTO - LUXURY vs CABRIO")
print("=" * 80)
print()

print("🚗 CARROS LUXURY (devem ir para Others):")
print("-" * 80)
luxury_ok = 0
luxury_fail = 0

for car_name, category in luxury_cars:
    group = map_category_to_group(category, car_name)
    
    if group == "Others":
        luxury_ok += 1
        status = "✅ Others"
        color = "\033[92m"  # Green
    else:
        luxury_fail += 1
        status = f"❌ {group}"
        color = "\033[91m"  # Red
    
    reset = "\033[0m"
    print(f"{color}{status:15}{reset} | {car_name:30} | Category: {category}")

print()
print("🎪 CARROS CABRIO (devem ir para G):")
print("-" * 80)
cabrio_ok = 0
cabrio_fail = 0

for car_name, category in cabrio_cars:
    group = map_category_to_group(category, car_name)
    
    if group == "G":
        cabrio_ok += 1
        status = "✅ G"
        color = "\033[92m"  # Green
    else:
        cabrio_fail += 1
        status = f"❌ {group}"
        color = "\033[91m"  # Red
    
    reset = "\033[0m"
    print(f"{color}{status:15}{reset} | {car_name:30} | Category: {category}")

print()
print("=" * 80)
print(f"RESUMO:")
print(f"  Luxury → Others: {luxury_ok}/{len(luxury_cars)} ✅")
print(f"  Cabrio → G:      {cabrio_ok}/{len(cabrio_cars)} ✅")
print(f"  Total OK:        {luxury_ok + cabrio_ok}/{len(luxury_cars) + len(cabrio_cars)}")
print("=" * 80)

if luxury_fail > 0 or cabrio_fail > 0:
    print("❌ FALHOU! Alguns carros não foram mapeados corretamente")
    sys.exit(1)
else:
    print("✅ SUCESSO! Todos os carros foram mapeados corretamente")
    sys.exit(0)
