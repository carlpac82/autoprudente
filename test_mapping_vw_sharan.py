#!/usr/bin/env python3
"""
Testar o mapeamento do VW Sharan
"""
import sys
sys.path.insert(0, '/Users/filipepacheco/CascadeProjects/RentalPriceTrackerPerDay')

from main import map_category_to_group

print("="*100)
print("TESTE: MAPEAMENTO VW SHARAN")
print("="*100)

# Testar vários cenários
scenarios = [
    {
        "name": "VW Sharan (Manual, categoria 7 Lugares)",
        "category": "7 Lugares",
        "car_name": "VW Sharan",
        "transmission": "Manual",
        "expected": "M1"
    },
    {
        "name": "VW Sharan (Automatic, categoria 7 Lugares)",
        "category": "7 Lugares",
        "car_name": "VW Sharan",
        "transmission": "Automatic",
        "expected": "M2"
    },
    {
        "name": "VW Sharan (VAZIO, categoria 7 Lugares) - Simula erro",
        "category": "7 Lugares",
        "car_name": "VW Sharan",
        "transmission": "",
        "expected": "M1"
    },
    {
        "name": "VW Sharan Auto (Automatic, categoria 7 Lugares)",
        "category": "7 Lugares",
        "car_name": "VW Sharan Auto",
        "transmission": "Automatic",
        "expected": "M2"
    },
    {
        "name": "Volkswagen Sharan (Manual)",
        "category": "7 Lugares",
        "car_name": "Volkswagen Sharan",
        "transmission": "Manual",
        "expected": "M1"
    },
]

print("\nTESTANDO CENÁRIOS:")
print("-"*100)

for scenario in scenarios:
    result = map_category_to_group(
        scenario["category"],
        scenario["car_name"],
        scenario["transmission"]
    )
    
    status = "✅" if result == scenario["expected"] else "❌"
    print(f"\n{status} {scenario['name']}")
    print(f"   Input: cat={scenario['category']}, car={scenario['car_name']}, trans={scenario['transmission']}")
    print(f"   Expected: {scenario['expected']}")
    print(f"   Got: {result}")
    
    if result != scenario["expected"]:
        print(f"   ⚠️  PROBLEMA: Esperava {scenario['expected']} mas obteve {result}")

print("\n" + "="*100)
