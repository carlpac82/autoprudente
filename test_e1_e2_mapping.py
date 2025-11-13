#!/usr/bin/env python3
"""Test E1/E2 mapping"""

import sys
sys.path.insert(0, '/Users/filipepacheco/CascadeProjects/RentalPriceTrackerPerDay')

from main import map_category_to_group, _map_category_to_group_code

print("\n🧪 TEST E1/E2 MAPPING\n")
print("="*80)

# Test direct mapping function
print("\n1️⃣ Testando _map_category_to_group_code:")
print("-"*80)

test_categories = [
    "MINI Auto",
    "MINI Automatic",
    "mini auto",
    "mini automatic",
    "ECONOMY Auto",
    "ECONOMY Automatic",
    "economy auto",
    "economy automatic",
]

for cat in test_categories:
    result = _map_category_to_group_code(cat)
    print(f"   {cat:30} → {result or 'NENHUM'}")

# Test full mapping function
print("\n2️⃣ Testando map_category_to_group (completa):")
print("-"*80)

test_cases = [
    ("MINI Auto", "Fiat 500 Auto", ""),
    ("MINI Automatic", "Peugeot 108 Auto", ""),
    ("ECONOMY Auto", "Opel Corsa Auto", ""),
    ("ECONOMY Automatic", "Ford Fiesta Auto", ""),
]

for category, car_name, transmission in test_cases:
    result = map_category_to_group(category, car_name, transmission)
    expected = "E1" if "MINI" in category else "E2"
    status = "✅" if result == expected else "❌"
    print(f"{status} {category:20} + {car_name:20} → {result} (esperado: {expected})")

print("\n" + "="*80 + "\n")
