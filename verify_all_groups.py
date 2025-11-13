#!/usr/bin/env python3
"""
Script para verificar se todos os carros estão nos grupos corretos
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from carjet_direct import VEHICLES, detect_category_from_car
from main import map_category_to_group

# Lista completa de carros que apareceram nos logs (amostra)
test_cars = [
    # B1 - MINI 4 Lugares (Manual)
    ('Toyota Aygo', ''),
    ('Fiat 500', ''),
    ('Citroen C1', ''),
    ('Peugeot 108', ''),
    ('Kia Picanto', ''),
    ('Opel Adam', ''),
    ('Renault Twingo', ''),
    ('Ford Ka', ''),
    
    # B2 - MINI 5 Lugares (Manual)
    ('Toyota Aygo X', ''),
    ('Fiat Panda', ''),
    ('Hyundai i10', ''),
    
    # E1 - MINI Auto
    ('Fiat 500 Electric', 'Electric'),
    ('Toyota Aygo Auto', 'Automatic'),
    ('Toyota Aygo X Auto', 'Automatic'),
    
    # D - Economy
    ('Renault Clio', ''),
    ('Peugeot 208', ''),
    ('Opel Corsa', ''),
    ('Ford Fiesta', ''),
    ('Seat Ibiza', ''),
    ('Hyundai i20', ''),
    ('Nissan Micra', ''),
    
    # E2 - Economy Auto
    ('Renault Clio Auto', 'Automatic'),
    ('Peugeot 208 Auto', 'Automatic'),
    ('Opel Corsa Auto', 'Automatic'),
    ('Ford Fiesta Auto', 'Automatic'),
    
    # J1 - Crossover
    ('Nissan Juke', ''),
    ('Fiat 500X', ''),
    ('MG ZS', ''),
    ('Hyundai Kona', ''),
    ('Mazda CX3', ''),
    ('Opel Crossland X', ''),
    ('Citroen C4', ''),
    
    # L1 - SUV Auto + Crossover Auto
    ('Citroen C4 Electric', 'Electric'),
    ('Opel Mokka Electric', 'Electric'),
    ('Peugeot 2008 Electric', 'Electric'),
    ('Volvo Xc40', 'Automatic'),
    ('Volvo Ex30 Electric', 'Electric'),
    ('Volvo Xc60', 'Automatic'),
    ('Mercedes Glc Coupe', 'Automatic'),
    
    # G - Cabrio
    ('Fiat 500 Cabrio', ''),
    ('Mini Cooper Cabrio', ''),
    
    # M1 - 7 Lugares (Manual)
    ('Dacia Jogger', ''),
    ('Peugeot Rifter', ''),
    ('Dacia Lodgy', ''),
    
    # M2 - 7 Lugares Auto (devem ter "Auto" no nome ou ser elétricos/híbridos)
    ('Dacia Jogger Auto', 'Automatic'),
    ('Peugeot Rifter Auto', 'Automatic'),
    ('Mercedes Glb 7 Seater Auto', 'Automatic'),
    ('Ford Galaxy Auto', 'Automatic'),
    ('Ford Tourneo Auto', 'Automatic'),
    ('Volkswagen Multivan Auto', 'Automatic'),
    ('VW Multivan Auto', 'Automatic'),
    ('Mercedes V Class Auto', 'Automatic'),
    ('Peugeot 5008 Auto', 'Automatic'),
    ('Renault Grand Scenic Auto', 'Automatic'),
    ('Citroen Grand Picasso Auto', 'Automatic'),
    ('Citroen C4 Picasso Auto', 'Automatic'),
    ('Skoda Kodiaq Auto', 'Automatic'),
    
    # N - 9 Lugares
    ('Ford Transit', ''),
    ('Mercedes Vito', ''),
    ('Opel Vivaro', ''),
    ('Toyota Proace', ''),
]

# Grupos esperados
expected_groups = {
    # B1
    'toyota aygo': 'B1',
    'fiat 500': 'B1',
    'citroen c1': 'B1',
    'peugeot 108': 'B1',
    'kia picanto': 'B1',
    'opel adam': 'B1',
    'renault twingo': 'B1',
    'ford ka': 'B1',
    
    # B2
    'toyota aygo x': 'B2',
    'fiat panda': 'B2',
    'hyundai i10': 'B2',
    
    # E1
    'fiat 500 electric': 'E1',
    'toyota aygo auto': 'E1',
    'toyota aygo x auto': 'E1',
    
    # D
    'renault clio': 'D',
    'peugeot 208': 'D',
    'opel corsa': 'D',
    'ford fiesta': 'D',
    'seat ibiza': 'D',
    'hyundai i20': 'D',
    'nissan micra': 'D',
    
    # E2
    'renault clio auto': 'E2',
    'peugeot 208 auto': 'E2',
    'opel corsa auto': 'E2',
    'ford fiesta auto': 'E2',
    
    # J1
    'nissan juke': 'J1',
    'fiat 500x': 'J1',
    'mg zs': 'J1',
    'hyundai kona': 'J1',
    'mazda cx3': 'J1',
    'opel crossland x': 'J1',
    'citroen c4': 'J1',
    
    # L1
    'citroen c4 electric': 'L1',
    'opel mokka electric': 'L1',
    'peugeot 2008 electric': 'L1',
    'volvo xc40': 'L1',
    'volvo ex30 electric': 'L1',
    'volvo xc60': 'L1',
    'mercedes glc coupe': 'L1',
    
    # G
    'fiat 500 cabrio': 'G',
    'mini cooper cabrio': 'G',
    
    # M1
    'dacia jogger': 'M1',
    'peugeot rifter': 'M1',
    'dacia lodgy': 'M1',
    
    # M2
    'dacia jogger auto': 'M2',
    'peugeot rifter auto': 'M2',
    'mercedes glb 7 seater auto': 'M2',
    'ford galaxy auto': 'M2',
    'ford tourneo auto': 'M2',
    'volkswagen multivan auto': 'M2',
    'vw multivan auto': 'M2',
    'mercedes v class auto': 'M2',
    'peugeot 5008 auto': 'M2',
    'renault grand scenic auto': 'M2',
    'citroen grand picasso auto': 'M2',
    'citroen c4 picasso auto': 'M2',
    'skoda kodiaq auto': 'M2',
    
    # N
    'ford transit': 'N',
    'mercedes vito': 'N',
    'opel vivaro': 'N',
    'toyota proace': 'N',
}

print("\n" + "="*120)
print("VERIFICAÇÃO COMPLETA DE GRUPOS")
print("="*120)

errors = []
correct = 0
total = 0

for car_name, transmission in test_cars:
    car_key = car_name.lower()
    
    # Detectar categoria
    category = detect_category_from_car(car_name, transmission)
    
    # Mapear para grupo
    group = map_category_to_group(category, car_name, transmission)
    
    # Verificar se está correto
    expected = expected_groups.get(car_key, '???')
    total += 1
    
    if group == expected:
        status = "✅"
        correct += 1
    else:
        status = "❌"
        errors.append((car_name, expected, group, category, transmission))
    
    trans_str = transmission or 'N/A'
    print(f"{status} {car_name:35} | Cat: {category:25} | Trans: {trans_str:10} | Expected: {expected:3} | Got: {group:3}")

print("\n" + "="*120)
print(f"RESUMO: {correct}/{total} corretos ({100*correct/total:.1f}%)")
print("="*120)

if errors:
    print("\n" + "="*120)
    print("ERROS ENCONTRADOS:")
    print("="*120)
    for car, expected, got, cat, trans in errors:
        print(f"❌ {car:35} | Expected: {expected:3} | Got: {got:3} | Cat: {cat:25} | Trans: {trans or 'N/A'}")
    print("="*120)
else:
    print("\n🎉 TODOS OS CARROS ESTÃO CORRETOS! 🎉")
