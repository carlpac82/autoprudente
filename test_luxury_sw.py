#!/usr/bin/env python3
"""
Testa mapeamento de MG EHS e Station Wagon Luxury
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from main import map_category_to_group

# Casos de teste
test_cases = [
    # MG EHS
    ("MG EHS 5 Door", "Crossover", "J1", "MG EHS manual = Crossover (J1)"),
    ("MG EHS", "Crossover", "J1", "MG EHS manual = Crossover (J1)"),
    ("MG EHS 5 Door Auto", "SUV Auto", "L1", "MG EHS auto = SUV Auto (L1)"),
    ("MG EHS Auto", "SUV Auto", "L1", "MG EHS auto = SUV Auto (L1)"),
    
    # Station Wagon Luxury → Others
    ("Mercedes C Class SW", "Luxury", "Others", "Mercedes C Class SW = Luxury → Others"),
    ("Mercedes C Class SW Auto", "Luxury", "Others", "Mercedes C Class SW Auto = Luxury → Others"),
    ("Mercedes E Class SW", "Luxury", "Others", "Mercedes E Class SW = Luxury → Others"),
    ("Mercedes E Class SW Auto", "Luxury", "Others", "Mercedes E Class SW Auto = Luxury → Others"),
    ("BMW 3 Series SW", "Luxury", "Others", "BMW 3 Series SW = Luxury → Others"),
    ("BMW 5 Series SW", "Luxury", "Others", "BMW 5 Series SW = Luxury → Others"),
    ("Volvo V60", "Luxury", "Others", "Volvo V60 = Luxury → Others"),
    ("Volvo V60 4X4", "Luxury", "Others", "Volvo V60 4X4 = Luxury → Others"),
    ("Volvo V60 4X4 Hybrid", "Luxury", "Others", "Volvo V60 4X4 Hybrid = Luxury → Others"),
]

print("=" * 80)
print("TESTE DE MAPEAMENTO - MG EHS E STATION WAGON LUXURY")
print("=" * 80)
print()

ok_count = 0
fail_count = 0

for car_name, category, expected, description in test_cases:
    group = map_category_to_group(category, car_name)
    
    if group == expected:
        ok_count += 1
        status = f"✅ {group}"
        color = "\033[92m"  # Green
    else:
        fail_count += 1
        status = f"❌ {group} (esperado: {expected})"
        color = "\033[91m"  # Red
    
    reset = "\033[0m"
    print(f"{color}{status:30}{reset} | {description}")

print()
print("=" * 80)
print(f"RESUMO: {ok_count}/{len(test_cases)} corretos")
print("=" * 80)

if fail_count > 0:
    print(f"❌ FALHOU! {fail_count} carros não foram mapeados corretamente")
    sys.exit(1)
else:
    print("✅ SUCESSO! MG EHS e Station Wagon Luxury mapeados corretamente")
    sys.exit(0)
