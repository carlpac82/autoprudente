#!/usr/bin/env python3
"""
Testa mapeamento de Toyota Corolla
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from main import map_category_to_group

# Casos de teste
test_cases = [
    # (car_name, category, expected_group, description)
    ("Toyota Corolla", "ECONOMY", "D", "Toyota Corolla manual = Economy (D)"),
    ("Toyota Corolla Auto", "ECONOMY Auto", "E2", "Toyota Corolla auto = Economy Auto (E2)"),
    ("Toyota Corolla SW Auto", "Station Wagon Auto", "L2", "Toyota Corolla SW auto = Station Wagon Auto (L2)"),
]

print("=" * 80)
print("TESTE DE MAPEAMENTO - TOYOTA COROLLA")
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
    print("✅ SUCESSO! Toyota Corolla mapeado corretamente")
    sys.exit(0)
