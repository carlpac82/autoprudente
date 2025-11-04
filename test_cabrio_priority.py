#!/usr/bin/env python3
"""
Testa que TODOS os carros com 'cabrio' no nome vão para Grupo G,
independentemente da categoria (Luxury, Cabrio, etc)
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from main import map_category_to_group

# Carros Cabrio com diferentes categorias - TODOS devem ir para G
test_cases = [
    # (car_name, category, expected_group)
    ("Fiat 500 Cabrio", "Cabrio", "G"),
    ("Fiat 500 Cabrio", "Luxury", "G"),  # Mesmo sendo Luxury, tem cabrio no nome
    ("Fiat 500 Cabrio", "MINI 4 Lugares", "G"),  # Mesmo sendo Mini, tem cabrio no nome
    ("Mini Cooper Cabrio", "Cabrio", "G"),
    ("Mini Cooper Cabrio", "Luxury", "G"),  # IMPORTANTE: Luxury + Cabrio = G
    ("Mini One Cabrio", "Cabrio", "G"),
    ("VW Beetle Cabrio", "Cabrio", "G"),
    ("BMW 4 Series Cabrio Auto", "Luxury", "G"),  # Luxury + Cabrio = G
    ("Mazda MX5 Cabrio Auto", "Cabrio", "G"),
    ("Peugeot 108 Cabrio", "Cabrio", "G"),
    ("Volkswagen T-Roc Cabrio", "SUV", "G"),  # SUV + Cabrio = G
    
    # Carros SEM cabrio no nome - devem ir para categoria original
    ("Mini Cooper", "Luxury", "Others"),  # Luxury sem cabrio = Others
    ("BMW 1 Series Auto", "Luxury", "Others"),
    ("Fiat 500", "MINI 4 Lugares", "B1"),  # Mini sem cabrio = B1
    ("Volkswagen T-Roc", "SUV", "F"),  # SUV sem cabrio = F
]

print("=" * 80)
print("TESTE DE PRIORIDADE - CABRIO vs CATEGORIA")
print("=" * 80)
print()

ok_count = 0
fail_count = 0

for car_name, category, expected in test_cases:
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
    has_cabrio = "🎪" if "cabrio" in car_name.lower() else "  "
    print(f"{has_cabrio} {color}{status:30}{reset} | {car_name:30} | Cat: {category:20}")

print()
print("=" * 80)
print(f"RESUMO: {ok_count}/{len(test_cases)} corretos")
print("=" * 80)

if fail_count > 0:
    print(f"❌ FALHOU! {fail_count} carros não foram mapeados corretamente")
    sys.exit(1)
else:
    print("✅ SUCESSO! Todos os carros Cabrio vão para Grupo G")
    print("✅ Carros Luxury SEM cabrio vão para Others")
    sys.exit(0)
