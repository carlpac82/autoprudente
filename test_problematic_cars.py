#!/usr/bin/env python3
"""
Testar carros problemáticos reportados pelo user
"""
import sys
sys.path.insert(0, '.')
from main import map_category_to_group, clean_car_name

# Carros problemáticos reportados
test_cases = [
    # GRUPO E1 - ERRADOS (deveriam ser outros grupos)
    ("Fiat 500X", "Crossover", "Manual"),  # Deveria ser J1, não E1
    
    # GRUPO E2 - DEVERIAM APARECER MAS NÃO APARECEM
    ("Opel Corsa Auto", "Economy Automatic", "Automatic"),  # Deveria ser E2
    ("Ford Fiesta Auto", "Economy Automatic", "Automatic"),  # Deveria ser E2
    ("Renault Clio Auto", "Economy Automatic", "Automatic"),  # Deveria ser E2
    ("Peugeot 208 Auto", "Economy Automatic", "Automatic"),  # Deveria ser E2
    
    # GRUPO F - ERRADOS (deveriam ser L1 ou outros)
    ("Opel Mokka Electric", "SUV Automatic", "Automatic"),  # Deveria ser L1
    ("MG ZS", "Crossover", "Manual"),  # Deveria ser J1
    ("Opel Crossland X", "Crossover", "Manual"),  # Deveria ser J1
    ("Mazda CX3", "Crossover", "Manual"),  # Deveria ser J1
    ("Toyota Hilux 4x4", "Luxury", "Manual"),  # Deveria ser X
    ("Hyundai Kona", "Crossover", "Manual"),  # Deveria ser J1
    
    # GRUPO J1 - ERRADOS (deveriam ser L1 ou M1)
    ("Citroen C4 Electric", "SUV Automatic", "Automatic"),  # Deveria ser L1
    ("Citroen C4 X Electric", "SUV Automatic", "Automatic"),  # Deveria ser L1
    ("Citroen C4 Picasso", "7 Seater", "Manual"),  # Deveria ser M1
    ("Peugeot 2008 Electric", "SUV Automatic", "Automatic"),  # Deveria ser L1
    ("Citroen C4 Grand Spacetourer", "7 Seater", "Manual"),  # Deveria ser M1
]

print("=" * 100)
print("TEST: CARROS PROBLEMÁTICOS")
print("=" * 100)
print()

# Mapa de grupo esperado
expected_map = {
    "Fiat 500X": "J1",
    "Opel Corsa Auto": "E2",
    "Ford Fiesta Auto": "E2",
    "Renault Clio Auto": "E2",
    "Peugeot 208 Auto": "E2",
    "Opel Mokka Electric": "L1",
    "MG ZS": "J1",
    "Opel Crossland X": "J1",
    "Mazda CX3": "J1",
    "Toyota Hilux 4x4": "X",
    "Hyundai Kona": "J1",
    "Citroen C4 Electric": "L1",
    "Citroen C4 X Electric": "L1",
    "Citroen C4 Picasso": "M1",
    "Peugeot 2008 Electric": "L1",
    "Citroen C4 Grand Spacetourer": "M1",
}

correct = 0
incorrect = 0

for car_name, category, transmission in test_cases:
    car_clean = clean_car_name(car_name)
    group_code = map_category_to_group(category, car_clean, transmission)
    
    expected = expected_map.get(car_name, "?")
    
    if group_code == expected:
        status = "✅"
        correct += 1
    else:
        status = f"❌ {group_code}"
        incorrect += 1
    
    print(f"{status:15s} | {car_name:30s} → {car_clean:30s} | Cat: {category:25s} | Expected: {expected} | Got: {group_code}")

print()
print("=" * 100)
print(f"RESUMO:")
print(f"  ✅ Corretos: {correct}/{len(test_cases)}")
print(f"  ❌ Incorretos: {incorrect}/{len(test_cases)}")
print("=" * 100)
