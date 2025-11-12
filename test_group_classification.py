#!/usr/bin/env python3
"""
Script de teste para verificar classificação de grupos após mudanças
"""

import sys
sys.path.insert(0, '/Users/filipepacheco/CascadeProjects/RentalPriceTrackerPerDay')

from main import map_category_to_group

# Casos de teste críticos
test_cases = [
    # GRUPO M2 (7 Seater Automatic) - CORRIGIDOS
    ("7 Seater Automatic", "VW Caddy Auto", "Automatic", "M2"),
    ("7 Seater", "VW Caddy Auto", "Automatic", "M2"),
    ("SUV", "Peugeot 5008 Auto", "Automatic", "M2"),
    ("7 Seater Automatic", "Dacia Jogger Auto", "Automatic", "M2"),
    ("7 Seater Automatic", "Opel Zafira Auto", "Automatic", "M2"),
    ("7 Seater", "Ford Galaxy Auto", "Automatic", "M2"),
    ("7 Seater", "Seat Alhambra Auto", "Automatic", "M2"),
    ("7 Seater", "VW Sharan Auto", "Automatic", "M2"),
    ("7 Seater Automatic", "Peugeot Rifter Auto", "Automatic", "M2"),
    ("7 Seater Automatic", "Renault Grand Scenic Auto", "Automatic", "M2"),
    
    # GRUPO N (9 Seater) - ADICIONADOS
    ("Van", "Mercedes Vito", "", "N"),
    ("Van", "Ford Transit", "", "N"),
    ("Van", "Renault Trafic", "", "N"),
    ("Van", "Toyota Proace", "", "N"),
    ("Van", "Opel Vivaro", "", "N"),
    ("Van", "Fiat Talento", "", "N"),
    ("9 Seater", "Ford Tourneo", "", "N"),
    ("Van", "Peugeot Traveller", "", "N"),
    
    # GRUPO E1 (Mini Automatic) - VERIFICAR
    ("Mini", "Fiat Panda Auto", "Automatic", "E1"),
    ("Mini", "Hyundai i10 Auto", "Automatic", "E1"),
    ("Mini", "Toyota Aygo Auto", "Automatic", "E1"),
    ("Mini", "Kia Picanto Auto", "Automatic", "E1"),
    ("Mini", "Fiat 500 Auto", "Automatic", "E1"),
    
    # GRUPO B2 (Mini 5 Doors) - Manual devem ir para B2
    ("Mini", "Fiat Panda", "Manual", "B2"),
    ("Mini", "Hyundai i10", "Manual", "B2"),
    
    # GRUPO L2 (Station Wagon Automatic) - VERIFICAR OCTAVIA
    ("Estate", "Skoda Octavia SW Auto", "Automatic", "L2"),
    ("Estate", "Peugeot 308 SW Auto", "Automatic", "L2"),
    ("Estate", "Ford Focus SW Auto", "Automatic", "L2"),
    ("Estate", "VW Golf Variant Auto", "Automatic", "L2"),
    
    # GRUPO J2 (Station Wagon) - Manual
    ("Estate", "Skoda Octavia SW", "Manual", "J2"),
    ("Estate", "Ford Focus SW", "Manual", "J2"),
    
    # GRUPO L1 (SUV Automatic)
    ("SUV", "Nissan Qashqai Auto", "Automatic", "L1"),
    ("SUV", "Peugeot 2008 Auto", "Automatic", "L1"),
    
    # GRUPO E2 (Economy Automatic)
    ("Economy", "Toyota Corolla Auto", "Automatic", "E2"),
    ("Economy", "Renault Clio Auto", "Automatic", "E2"),
]

def test_classification():
    """Testa a classificação de grupos"""
    print("\n" + "="*80)
    print("🧪 TESTE DE CLASSIFICAÇÃO DE GRUPOS")
    print("="*80 + "\n")
    
    passed = 0
    failed = 0
    
    for category, car_name, transmission, expected_group in test_cases:
        result = map_category_to_group(category, car_name, transmission)
        
        if result == expected_group:
            status = "✅ PASS"
            passed += 1
        else:
            status = f"❌ FAIL (got {result})"
            failed += 1
        
        print(f"{status:20} | {car_name:35} | Cat: {category:25} | Expected: {expected_group:3} | Got: {result:3}")
    
    print("\n" + "="*80)
    print(f"📊 RESULTADOS: {passed} passed, {failed} failed ({passed}/{len(test_cases)} = {passed/len(test_cases)*100:.1f}%)")
    print("="*80 + "\n")
    
    return failed == 0

if __name__ == "__main__":
    success = test_classification()
    sys.exit(0 if success else 1)
