#!/usr/bin/env python3
"""
Debug: Testar mapeamento de grupos com exemplos reais
"""

import sys
sys.path.insert(0, '.')
from main import map_category_to_group, clean_car_name

# Exemplos de carros que provavelmente estão em "Others"
test_cases = [
    # Mini 4 lugares (B1)
    ("Fiat 500", "Mini"),
    ("Fiat 500 ou similar", "Mini"),
    ("Peugeot 108", "Mini"),
    ("Citroen C1", "Mini"),
    ("Toyota Aygo", "Mini"),
    ("VW Up", "Mini"),
    
    # Mini 5 lugares (B2)
    ("Fiat Panda", "Mini"),
    ("Hyundai i10", "Mini"),
    ("Kia Picanto", "Mini"),
    
    # Economy (D)
    ("Renault Clio", "Economy"),
    ("Peugeot 208", "Economy"),
    ("Ford Fiesta", "Economy"),
    ("Opel Corsa", "Economy"),
    
    # Mini Automatic (E1)
    ("Fiat 500 Auto", "Mini Automatic"),
    ("Fiat 500 Automático", "Mini Automatic"),
    
    # Economy Automatic (E2)
    ("Renault Clio Auto", "Economy Automatic"),
    ("Opel Corsa Auto", "Economy Automatic"),
    
    # SUV (F)
    ("Peugeot 2008", "SUV"),
    ("Nissan Juke", "SUV"),
    ("Renault Captur", "SUV"),
    
    # Crossover (J1)
    ("Fiat 500X", "Crossover"),
    ("Citroen C3 Aircross", "Crossover"),
    
    # Station Wagon (J2)
    ("Seat Leon SW", "Estate/Station Wagon"),
    ("Renault Megane SW", "Estate/Station Wagon"),
    
    # SUV Auto (L1) - PROBLEMÁTICOS
    ("Volkswagen T-Roc", "SUV"),  # Manual F ou Auto L1?
    ("Volkswagen T-Roc Auto", "SUV Automatic"),  # Deve ser L1
    ("Peugeot 3008 Auto", "SUV Automatic"),  # Deve ser L1
    
    # 7 Lugares Auto (M2) - PROBLEMÁTICO
    ("Peugeot Rifter Auto", "7 Seater Automatic"),  # DEVE SER M2!
    ("Peugeot Rifter", "7 Seater"),  # Manual M1
    ("Citroen Grand Spacetourer Auto", "7 Seater Automatic"),  # M2
    
    # Crossover vs SUV (J1 vs F)
    ("Hyundai Kona", "SUV"),  # Deve ser J1 (Crossover)
    ("Mazda CX3", "SUV"),  # Deve ser J1 (Crossover)
    ("MG ZS", "SUV"),  # Deve ser J1 (Crossover)
    ("Opel Mokka", "SUV"),  # Deve ser J1 (Crossover)
    
    # SUV Automatic (L1)
    ("Peugeot 3008 Auto", "SUV Automatic"),
    
    # Station Wagon Automatic (L2)
    ("Toyota Corolla SW Auto", "Station Wagon Automatic"),
    
    # 7 Seater (M1)
    ("Dacia Lodgy", "7 Seater"),
    ("Peugeot Rifter", "7 Seater"),
    
    # 7 Seater Automatic (M2)
    ("Renault Grand Scenic Auto", "7 Seater Automatic"),
    
    # 9 Seater (N)
    ("Ford Tourneo", "9 Seater"),
    ("Mercedes Vito", "9 Seater"),
]

print("=" * 100)
print("DEBUG: MAPEAMENTO DE GRUPOS")
print("=" * 100)
print()

# Testar cada caso
correct = 0
incorrect = 0
others = 0

for car_name, expected_category in test_cases:
    car_clean = clean_car_name(car_name)
    group_code = map_category_to_group(expected_category, car_clean)
    
    # Determinar grupo esperado baseado na categoria
    expected_groups = {
        "Mini": ["B1", "B2"],  # Pode ser B1 ou B2 dependendo do modelo
        "Mini Automatic": ["E1"],
        "Economy": ["D"],
        "Economy Automatic": ["E2"],
        "SUV": ["F"],
        "Crossover": ["J1"],
        "Estate/Station Wagon": ["J2"],
        "SUV Automatic": ["L1"],
        "Station Wagon Automatic": ["L2"],
        "7 Seater": ["M1"],
        "7 Seater Automatic": ["M2"],
        "9 Seater": ["N"],
    }
    
    expected = expected_groups.get(expected_category, [])
    
    if group_code == "Others":
        status = "❌ Others"
        others += 1
    elif group_code in expected:
        status = "✅"
        correct += 1
    else:
        status = f"⚠️  {group_code}"
        incorrect += 1
    
    print(f"{status:15s} | {car_name:40s} → {car_clean:40s} | Cat: {expected_category:25s} | Group: {group_code}")

print()
print("=" * 100)
print(f"RESULTADOS:")
print(f"  ✅ Corretos: {correct}/{len(test_cases)}")
print(f"  ⚠️  Incorretos: {incorrect}/{len(test_cases)}")
print(f"  ❌ Others: {others}/{len(test_cases)}")
print("=" * 100)
