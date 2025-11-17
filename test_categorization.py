#!/usr/bin/env python3
"""
Testar categorização de carros automáticos
"""
import sys
sys.path.insert(0, '/Users/filipepacheco/CascadeProjects/RentalPriceTrackerPerDay')

from carjet_direct import detect_category_from_car, map_category_to_group_code

# Testes
test_cases = [
    # (car_name, transmission, expected_category, expected_group)
    ("Seat Arona Auto", "Automatic", "SUV Auto", "L1"),
    ("Nissan Qashqai Auto", "Automatic", "SUV Auto", "L1"),
    ("Ford Focus SW Auto", "Automatic", "Station Wagon Auto", "L2"),
    ("Peugeot 308 SW Auto", "Automatic", "Station Wagon Auto", "L2"),
    ("Citroen C4 Picasso Auto", "Automatic", "7 Lugares Auto", "M2"),
    ("Renault Grand Scenic Auto", "Automatic", "7 Lugares Auto", "M2"),
    ("Toyota Aygo Auto", "Automatic", "MINI Auto", "E1"),
    ("Kia Picanto Auto", "Automatic", "MINI Auto", "E1"),
    ("Seat Arona Auto", "Automatic", "SUV Auto", "L1"),
    ("Peugeot 308 Auto", "Automatic", "ECONOMY Auto", "E2"),
    ("Citroen C3 Auto", "Automatic", "MINI 5 Lugares Auto", "E1"),
    ("VW Polo Auto", "Automatic", "MINI 5 Lugares Auto", "E1"),
    
    # Manuais para comparação
    ("Seat Arona", "Manual", "SUV", "F"),
    ("Ford Focus SW", "Manual", "Station Wagon", "J2"),
    ("Peugeot 308", "Manual", "ECONOMY", "D"),
]

print("🧪 TESTE DE CATEGORIZAÇÃO\n")
print("=" * 100)

errors = []
for car_name, transmission, expected_cat, expected_group in test_cases:
    category = detect_category_from_car(car_name, transmission)
    group = map_category_to_group_code(category)
    
    cat_ok = "✅" if category == expected_cat else "❌"
    group_ok = "✅" if group == expected_group else "❌"
    
    print(f"\n{car_name} ({transmission})")
    print(f"  Categoria: {cat_ok} {category} (esperado: {expected_cat})")
    print(f"  Grupo:     {group_ok} {group} (esperado: {expected_group})")
    
    if category != expected_cat or group != expected_group:
        errors.append({
            'car': car_name,
            'got_cat': category,
            'expected_cat': expected_cat,
            'got_group': group,
            'expected_group': expected_group
        })

print("\n" + "=" * 100)

if errors:
    print(f"\n❌ {len(errors)} ERROS ENCONTRADOS:")
    for err in errors:
        print(f"  - {err['car']}: categoria={err['got_cat']} (esperado {err['expected_cat']}), grupo={err['got_group']} (esperado {err['expected_group']})")
else:
    print(f"\n✅ TODOS OS TESTES PASSARAM!")
