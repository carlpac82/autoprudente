#!/usr/bin/env python3
"""
Testa mapeamento de VW Tiguan e Skoda Karoq
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from main import map_category_to_group

# Casos de teste
test_cases = [
    # (car_name, category, expected_group, description)
    ("Volkswagen Tiguan", "SUV", "F", "VW Tiguan manual = SUV (F)"),
    ("VW Tiguan", "SUV", "F", "VW Tiguan manual = SUV (F)"),
    ("Volkswagen Tiguan Auto", "SUV Auto", "L1", "VW Tiguan auto = SUV Auto (L1)"),
    ("VW Tiguan Auto", "SUV Auto", "L1", "VW Tiguan auto = SUV Auto (L1)"),
    
    ("Skoda Karoq", "Crossover", "J1", "Skoda Karoq manual = Crossover (J1)"),
    ("Skoda Karoq Auto", "SUV Auto", "L1", "Skoda Karoq auto = SUV Auto (L1)"),
]

print("=" * 80)
print("TESTE DE MAPEAMENTO - VW TIGUAN E SKODA KAROQ")
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
    print("✅ SUCESSO! VW Tiguan e Skoda Karoq mapeados corretamente")
    sys.exit(0)
