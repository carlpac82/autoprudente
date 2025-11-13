#!/usr/bin/env python3
"""
Script para testar carros problemáticos em L1 e M1
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from carjet_direct import VEHICLES
from main import map_category_to_group

# Carros problemáticos do L1 que estão como Luxury mas deveriam ser SUV Auto
l1_problematic_cars = [
    ('Volvo Xc40', 'Luxury'),
    ('Volvo Ex30 Electric', 'Luxury'),
    ('Volvo Xc60', 'Luxury'),
    ('Mercedes Glc Coupe', 'Luxury'),
]

# Carros do M1 para verificar se são automáticos
m1_cars_to_check = [
    'Dacia Jogger',
    'Peugeot Rifter',
    'Opel Zafira',
    'Volkswagen Caddy',
    'Volkswagen Sharan',
    'Peugeot 5008',
    'Dacia Lodgy',
    'Ford Galaxy',
    'Ford Tourneo',
    'Mercedes Glb 7 Seater',
    'Volkswagen Multivan',
    'Renault Grand Scenic',
    'Citroen Grand Picasso',
    'Skoda Kodiaq',
    'Mercedes V Class',
    'Mercedes V Class Auto',  # Este já tem "Auto" no nome
]

def check_vehicles_dict():
    """Verificar como os carros estão no dicionário VEHICLES"""
    print("\n" + "="*100)
    print("VERIFICAÇÃO NO DICIONÁRIO VEHICLES")
    print("="*100)
    
    print("\n1️⃣ CARROS L1 PROBLEMÁTICOS (devem ser SUV Auto, não Luxury):")
    print("-" * 100)
    for car_name, current_cat in l1_problematic_cars:
        car_key = car_name.lower()
        if car_key in VEHICLES:
            actual_cat = VEHICLES[car_key]
            status = "❌" if actual_cat == current_cat else "✅"
            print(f"{status} {car_name:30} → VEHICLES: '{actual_cat:20}' | Esperado: 'SUV Auto' (L1)")
        else:
            print(f"⚠️  {car_name:30} → NÃO ENCONTRADO em VEHICLES")
    
    print("\n2️⃣ CARROS M1 - Verificar quais têm versão Auto parametrizada:")
    print("-" * 100)
    for car_name in m1_cars_to_check:
        car_key = car_name.lower()
        car_key_auto = f"{car_key} auto"
        
        has_manual = car_key in VEHICLES
        has_auto = car_key_auto in VEHICLES
        
        manual_cat = VEHICLES.get(car_key, "N/A")
        auto_cat = VEHICLES.get(car_key_auto, "N/A")
        
        # Determinar se é automático pelo nome
        is_auto_name = 'auto' in car_key
        
        if is_auto_name:
            expected = "M2"
            icon = "🔴" if auto_cat != "7 Lugares Auto" else "✅"
        else:
            expected = "M1 (manual) ou M2 (auto)"
            icon = "📋"
        
        print(f"{icon} {car_name:30} | Manual: {manual_cat:20} | Auto: {auto_cat:20} | Expected: {expected}")

def test_mapping():
    """Testar mapeamento dos carros problemáticos"""
    print("\n" + "="*100)
    print("TESTE DE MAPEAMENTO")
    print("="*100)
    
    print("\n1️⃣ CARROS L1 (devem mapear para L1, não X):")
    print("-" * 100)
    for car_name, category in l1_problematic_cars:
        # Testar com transmissão automática
        group = map_category_to_group(category, car_name, "Automatic")
        expected = "L1"
        status = "✅" if group == expected else f"❌ Got: {group}"
        print(f"{status:15} | {car_name:30} | Cat: {category:20} | Expected: {expected} | Transmission: Automatic")
    
    print("\n2️⃣ CARROS M1/M2 - Verificar mapeamento com transmission='Automatic':")
    print("-" * 100)
    for car_name in m1_cars_to_check:
        car_key = car_name.lower()
        
        # Se o nome tem "auto", deve ir para M2 mesmo sem transmission
        if 'auto' in car_key:
            category = "7 Lugares Auto"
            expected = "M2"
            transmission = ""
        else:
            # Testar com transmission="Automatic" - deve ir para M2
            category = "7 Lugares"
            expected = "M2"
            transmission = "Automatic"
        
        group = map_category_to_group(category, car_name, transmission)
        status = "✅" if group == expected else f"❌ Got: {group}"
        trans_info = f"Trans: {transmission or 'N/A':10}"
        print(f"{status:15} | {car_name:30} | Cat: {category:20} | {trans_info} | Expected: {expected}")

if __name__ == "__main__":
    check_vehicles_dict()
    test_mapping()
