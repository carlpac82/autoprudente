#!/usr/bin/env python3
"""
Script para testar problemas do Grupo B1 e E1
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from carjet_direct import VEHICLES
from main import map_category_to_group

# Carros para testar
test_cars = [
    # Fiat 500 variations
    ('Fiat 500', 'MINI 4 Lugares', 'Manual', 'B1'),
    ('Fiat 500 Auto', 'MINI Auto', 'Automatic', 'E1'),
    ('Fiat 500 Electric', 'MINI Auto', 'Electric', 'E1'),  # ⚠️ NÃO ESTÁ NO VEHICLES
    ('Fiat 500 Hybrid', 'MINI 4 Lugares', 'Manual', 'B1'),
    
    # Toyota Aygo variations
    ('Toyota Aygo', 'MINI 4 Lugares', 'Manual', 'B1'),
    ('Toyota Aygo Auto', 'MINI Auto', 'Automatic', 'E1'),
    ('Toyota Aygo X', 'MINI 5 Lugares', 'Manual', 'B2'),
    ('Toyota Aygo X Auto', 'MINI Auto', 'Automatic', 'E1'),
]

print("\n" + "="*100)
print("VERIFICAÇÃO NO DICIONÁRIO VEHICLES")
print("="*100)

for car_name, expected_category, transmission, expected_group in test_cars:
    car_key = car_name.lower()
    
    if car_key in VEHICLES:
        actual_category = VEHICLES[car_key]
        status = "✅" if actual_category == expected_category else f"❌ Got: {actual_category}"
    else:
        status = "⚠️  NÃO ENCONTRADO"
        actual_category = "N/A"
    
    print(f"{status:30} | {car_name:30} | Expected: {expected_category:20} | Transmission: {transmission:10}")

print("\n" + "="*100)
print("TESTE DE MAPEAMENTO")
print("="*100)

for car_name, expected_category, transmission, expected_group in test_cars:
    car_key = car_name.lower()
    
    # Se o carro está no VEHICLES, usar a categoria de lá
    if car_key in VEHICLES:
        category = VEHICLES[car_key]
    else:
        # Usar a categoria esperada como fallback
        category = expected_category
    
    # Mapear
    group = map_category_to_group(category, car_name, transmission)
    
    status = "✅" if group == expected_group else f"❌ Got: {group}"
    print(f"{status:15} | {car_name:30} | Cat: {category:20} | Trans: {transmission:10} | Expected: {expected_group}")

print("\n" + "="*100)
print("VARIAÇÕES DE NOMES NO SCRAPING")
print("="*100)
print("Verificar se o scraping da CarJet retorna:")
print("  • 'Fiat 500 Electric' ou 'Fiat 500 e' ou 'Fiat 500e'?")
print("  • 'Toyota Aygo Auto' ou 'Toyota Aygo'?")
print("  • 'Toyota Aygo X Auto' ou 'Toyota Aygo X'?")
print("\n⚠️  É CRUCIAL que o scraping capture o sufixo 'Auto' ou 'Electric' no nome!")
print("="*100)
