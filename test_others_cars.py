#!/usr/bin/env python3
"""
Script para testar quais carros aparecem em "Others"
"""

from main import map_category_to_group
from carjet_direct import VEHICLES

def test_vehicles_dict():
    """Testa todos os carros do dicionário VEHICLES"""
    print("=" * 80)
    print("TESTE 1: Carros do dicionário VEHICLES")
    print("=" * 80)
    
    others_count = 0
    others_list = []
    total = len(VEHICLES)
    
    for car_name, category in VEHICLES.items():
        group = map_category_to_group(category, car_name)
        if group == "Others":
            others_count += 1
            others_list.append((car_name, category))
    
    print(f"\nTotal de carros no VEHICLES: {total}")
    print(f"Carros em 'Others': {others_count}")
    print(f"Percentagem: {(others_count/total)*100:.1f}%\n")
    
    if others_list:
        print("Carros que aparecem em 'Others':")
        print("-" * 80)
        for car, cat in sorted(others_list):
            print(f"  • {car:40} | Categoria: {cat}")
    else:
        print("✅ Nenhum carro do VEHICLES aparece em 'Others'!")
    
    return others_count, total

def test_common_categories():
    """Testa categorias comuns do CarJet"""
    print("\n" + "=" * 80)
    print("TESTE 2: Categorias Comuns do CarJet (Inglês)")
    print("=" * 80)
    
    # Categorias que o CarJet costuma retornar
    test_cases = [
        # Mini categories
        ("Mini 4 Seats", "Fiat 500"),
        ("Mini 5 Seats", "Fiat Panda"),
        ("Mini Automatic", "Fiat 500 Auto"),
        ("Mini Auto", "Hyundai i10 Auto"),
        
        # Economy
        ("Economy", "Renault Clio"),
        ("Economy Automatic", "Renault Clio Auto"),
        ("Compact", "Seat Ibiza"),
        ("Compact Automatic", "Opel Corsa Auto"),
        
        # SUV
        ("SUV", "Toyota Chr"),
        ("SUV Automatic", "Nissan Qashqai Auto"),
        ("Jeep", "Dacia Duster"),
        
        # Station Wagon
        ("Station Wagon", "Skoda Octavia SW"),
        ("Station Wagon Automatic", "VW Passat SW Auto"),
        ("Estate", "BMW 3 Series Touring"),
        
        # Crossover
        ("Crossover", "Nissan Juke"),
        
        # Luxury/Premium
        ("Luxury", "BMW 3 Series"),
        ("Premium", "Mercedes C Class"),
        ("Cabrio", "BMW 4 Series Cabrio"),
        ("Cabriolet", "Audi A5 Cabriolet"),
        
        # 7 Seater
        ("7 Seats", "Peugeot 5008"),
        ("7 Seater", "Citroen Berlingo"),
        ("7 Seats Automatic", "VW Caddy Auto"),
        ("People Carrier", "Renault Kangoo"),
        ("MPV", "Dacia Jogger"),
        
        # 9 Seater
        ("9 Seats", "Mercedes Vito"),
        ("9 Seater", "VW Caravelle"),
        ("9 Seats Automatic", "Ford Transit Auto"),
        ("Minivan", "Renault Trafic"),
        ("Van", "Peugeot Expert"),
    ]
    
    others_count = 0
    success_count = 0
    
    print("\nResultados:")
    print("-" * 80)
    
    for category, car in test_cases:
        group = map_category_to_group(category, car)
        if group == "Others":
            others_count += 1
            print(f"❌ {category:30} + {car:30} → Others")
        else:
            success_count += 1
            print(f"✅ {category:30} + {car:30} → {group}")
    
    total = len(test_cases)
    print(f"\n{'=' * 80}")
    print(f"Total testado: {total}")
    print(f"Sucesso: {success_count} ({(success_count/total)*100:.1f}%)")
    print(f"Others: {others_count} ({(others_count/total)*100:.1f}%)")
    
    return others_count, total

def test_edge_cases():
    """Testa casos especiais e edge cases"""
    print("\n" + "=" * 80)
    print("TESTE 3: Casos Especiais e Edge Cases")
    print("=" * 80)
    
    test_cases = [
        # Carros sem categoria (só nome)
        ("", "Toyota Aygo"),
        ("", "Fiat 500"),
        ("", "BMW 3 Series"),
        ("", "Mercedes Vito"),
        
        # Categorias em português
        ("MINI 4 Lugares", "Fiat 500"),
        ("MINI 5 Lugares", "Fiat Panda"),
        ("ECONOMY", "Renault Clio"),
        ("SUV Auto", "Toyota Chr Auto"),
        ("7 Lugares", "Peugeot 5008"),
        
        # Categorias mistas/estranhas
        ("Mini", "Fiat Panda"),
        ("Economy 5 Doors", "Seat Ibiza"),
        ("SUV 5 Doors", "Nissan Qashqai"),
        
        # Carros elétricos/híbridos
        ("Economy", "Peugeot E-208 Electric"),
        ("SUV", "Toyota Chr Hybrid"),
        ("Compact", "Renault Zoe Electric"),
    ]
    
    others_count = 0
    success_count = 0
    
    print("\nResultados:")
    print("-" * 80)
    
    for category, car in test_cases:
        cat_display = category if category else "(empty)"
        group = map_category_to_group(category, car)
        if group == "Others":
            others_count += 1
            print(f"❌ {cat_display:30} + {car:30} → Others")
        else:
            success_count += 1
            print(f"✅ {cat_display:30} + {car:30} → {group}")
    
    total = len(test_cases)
    print(f"\n{'=' * 80}")
    print(f"Total testado: {total}")
    print(f"Sucesso: {success_count} ({(success_count/total)*100:.1f}%)")
    print(f"Others: {others_count} ({(others_count/total)*100:.1f}%)")
    
    return others_count, total

def main():
    print("\n" + "🔍 " * 20)
    print("TESTE COMPLETO: Quais carros aparecem em 'Others'")
    print("🔍 " * 20 + "\n")
    
    # Teste 1: VEHICLES
    others1, total1 = test_vehicles_dict()
    
    # Teste 2: Categorias comuns
    others2, total2 = test_common_categories()
    
    # Teste 3: Edge cases
    others3, total3 = test_edge_cases()
    
    # Sumário final
    print("\n" + "=" * 80)
    print("📊 SUMÁRIO FINAL")
    print("=" * 80)
    print(f"\nTeste 1 (VEHICLES):        {others1}/{total1} em Others ({(others1/total1)*100:.1f}%)")
    print(f"Teste 2 (Categorias):      {others2}/{total2} em Others ({(others2/total2)*100:.1f}%)")
    print(f"Teste 3 (Edge Cases):      {others3}/{total3} em Others ({(others3/total3)*100:.1f}%)")
    
    total_others = others1 + others2 + others3
    total_tested = total1 + total2 + total3
    
    print(f"\n{'=' * 80}")
    print(f"TOTAL GERAL:               {total_others}/{total_tested} em Others ({(total_others/total_tested)*100:.1f}%)")
    print(f"Taxa de Sucesso:           {((total_tested-total_others)/total_tested)*100:.1f}%")
    print("=" * 80)
    
    if total_others == 0:
        print("\n🎉 PERFEITO! Nenhum carro aparece em 'Others'!")
    elif total_others < 10:
        print(f"\n✅ EXCELENTE! Apenas {total_others} carros em 'Others'")
    elif total_others < 30:
        print(f"\n👍 BOM! {total_others} carros em 'Others' (aceitável)")
    else:
        print(f"\n⚠️  ATENÇÃO! {total_others} carros em 'Others' (precisa melhorias)")

if __name__ == "__main__":
    main()
