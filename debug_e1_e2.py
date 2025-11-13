#!/usr/bin/env python3
"""Debug script para verificar nomes de carros E1 e E2"""

from carjet_direct import scrape_carjet_direct, VEHICLES
from datetime import datetime, timedelta
import re

def normalize_name(name: str) -> str:
    """Normaliza nome do carro"""
    name = name.lower().strip()
    name = re.sub(r'\s+(ou\s*similar|or\s*similar).*$', '', name, flags=re.IGNORECASE)
    name = re.sub(r'\s*\|\s*.*$', '', name)
    name = re.sub(r'\s+', ' ', name).strip()
    return name

def main():
    print("\n🔍 DEBUG: Verificando carros E1 e E2\n")
    print("="*80)
    
    # Fazer scraping
    location = "Faro, Aeroporto de Faro (FAO)"
    start_date = datetime.now() + timedelta(days=7)
    end_date = start_date + timedelta(days=7)
    
    print(f"📍 Local: {location}")
    print(f"📅 Datas: {start_date.strftime('%d/%m/%Y')} → {end_date.strftime('%d/%m/%Y')}\n")
    
    cars = scrape_carjet_direct(location, start_date, end_date)
    print(f"✅ {len(cars)} carros encontrados\n")
    
    # Filtrar carros com "auto" no nome (potenciais E1/E2)
    auto_cars = []
    for car in cars:
        name = car.get('car', '')
        normalized = normalize_name(name)
        
        # Verificar se tem "auto" no nome
        if 'auto' in normalized and not any(x in normalized for x in ['autoprudente', 'automobile']):
            auto_cars.append({
                'original': name,
                'normalized': normalized,
                'category': car.get('category', 'N/A'),
                'group': car.get('group', 'N/A'),
                'price': car.get('price', 'N/A'),
                'supplier': car.get('supplier', 'N/A')
            })
    
    print(f"🚗 CARROS COM 'AUTO' NO NOME: {len(auto_cars)}\n")
    print("="*80)
    
    # Agrupar por tamanho (mini vs economy)
    mini_autos = []
    economy_autos = []
    
    for car in auto_cars:
        norm = car['normalized']
        
        # Verificar se é MINI
        mini_keywords = ['fiat 500', 'peugeot 108', 'citroen c1', 'toyota aygo', 
                         'kia picanto', 'vw up', 'volkswagen up', 'fiat panda', 
                         'hyundai i10', 'mitsubishi spacestar']
        
        is_mini = any(k in norm for k in mini_keywords)
        
        if is_mini:
            mini_autos.append(car)
        else:
            # Verificar se é economy
            economy_keywords = ['opel corsa', 'ford fiesta', 'peugeot 208', 'peugeot e-208',
                               'renault clio', 'seat ibiza', 'citroen c3', 'nissan micra']
            is_economy = any(k in norm for k in economy_keywords)
            if is_economy:
                economy_autos.append(car)
    
    # Mostrar MINI AUTO (E1)
    print(f"\n🔵 MINI AUTO (esperado E1) - {len(mini_autos)} carros:\n")
    for car in mini_autos:
        in_vehicles = "✅" if car['normalized'] in VEHICLES else "❌"
        print(f"{in_vehicles} {car['normalized']}")
        print(f"   Original: {car['original']}")
        print(f"   Category: {car['category']}")
        print(f"   Group: {car['group']}")
        print(f"   Supplier: {car['supplier']}")
        print(f"   Price: {car['price']}")
        
        # Ver se está no VEHICLES
        if car['normalized'] in VEHICLES:
            print(f"   ✅ VEHICLES: {VEHICLES[car['normalized']]}")
        else:
            # Buscar parcial
            for k in VEHICLES.keys():
                if k in car['normalized'] and len(k) >= 5:
                    print(f"   🔍 VEHICLES PARCIAL: '{k}' → {VEHICLES[k]}")
                    break
        print()
    
    # Mostrar ECONOMY AUTO (E2)
    print(f"\n🟢 ECONOMY AUTO (esperado E2) - {len(economy_autos)} carros:\n")
    for car in economy_autos:
        in_vehicles = "✅" if car['normalized'] in VEHICLES else "❌"
        print(f"{in_vehicles} {car['normalized']}")
        print(f"   Original: {car['original']}")
        print(f"   Category: {car['category']}")
        print(f"   Group: {car['group']}")
        print(f"   Supplier: {car['supplier']}")
        print(f"   Price: {car['price']}")
        
        # Ver se está no VEHICLES
        if car['normalized'] in VEHICLES:
            print(f"   ✅ VEHICLES: {VEHICLES[car['normalized']]}")
        else:
            # Buscar parcial
            for k in VEHICLES.keys():
                if k in car['normalized'] and len(k) >= 5:
                    print(f"   🔍 VEHICLES PARCIAL: '{k}' → {VEHICLES[k]}")
                    break
        print()
    
    print("="*80)
    print(f"\n📊 RESUMO:")
    print(f"   - Total com 'auto': {len(auto_cars)}")
    print(f"   - Mini Auto (E1): {len(mini_autos)}")
    print(f"   - Economy Auto (E2): {len(economy_autos)}")
    print(f"   - Outros auto: {len(auto_cars) - len(mini_autos) - len(economy_autos)}")
    print("\n" + "="*80 + "\n")

if __name__ == "__main__":
    main()
