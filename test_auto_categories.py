#!/usr/bin/env python3
"""
Teste para verificar categorização de automáticos
"""

from carjet_direct import detect_category_from_car, map_category_to_group_code

# Casos de teste de automáticos que devem ser E1 ou E2
test_cases = [
    # E1 - MINI Auto
    ("Fiat 500", "Automatic", "E1"),
    ("Citroen C1", "Automatic", "E1"),
    ("Toyota Aygo", "Automatic", "E1"),
    ("Fiat Panda", "Automatic", "E1"),
    ("Volkswagen UP", "Automatic", "E1"),
    
    # E2 - Economy Auto
    ("Renault Clio", "Automatic", "E2"),
    ("Peugeot 208", "Automatic", "E2"),
    ("Ford Fiesta", "Automatic", "E2"),
    ("Seat Ibiza", "Automatic", "E2"),
    ("Hyundai i20", "Automatic", "E2"),
    ("Opel Corsa", "Automatic", "E2"),
    ("Peugeot 308", "Automatic", "E2"),
    
    # Manuais devem ser B1, B2 ou D
    ("Fiat 500", "Manual", "B1"),
    ("Citroen C1", "Manual", "B1"),
    ("Toyota Aygo", "Manual", "B2"),
    ("Renault Clio", "Manual", "D"),
    ("Peugeot 208", "Manual", "D"),
]

print("=" * 80)
print("TESTE DE CATEGORIZAÇÃO DE AUTOMÁTICOS")
print("=" * 80)

errors = []

for car, trans, expected_group in test_cases:
    category = detect_category_from_car(car, trans)
    group = map_category_to_group_code(category)
    
    status = "✅" if group == expected_group else "❌"
    
    print(f"{status} {car:25} {trans:10} → {category:25} → {group:4} (esperado: {expected_group})")
    
    if group != expected_group:
        errors.append({
            'car': car,
            'trans': trans,
            'category': category,
            'group': group,
            'expected': expected_group
        })

print("\n" + "=" * 80)
if errors:
    print(f"❌ {len(errors)} ERROS ENCONTRADOS:")
    print("=" * 80)
    for err in errors:
        print(f"  {err['car']} ({err['trans']})")
        print(f"    Categoria: {err['category']}")
        print(f"    Grupo: {err['group']} (esperado: {err['expected']})")
        print()
else:
    print("✅ TODOS OS TESTES PASSARAM!")
    print("=" * 80)
