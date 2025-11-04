#!/usr/bin/env python3
"""
Script para verificar a distribuição de carros por grupo
"""

from main import map_category_to_group
from carjet_direct import VEHICLES
from collections import defaultdict

# Mapeamento de códigos para nomes descritivos
GROUP_NAMES = {
    "B1": "Mini 4 Seats (Manual)",
    "B2": "Mini 5 Seats (Manual)",
    "D": "Economy",
    "E1": "Mini Automatic",
    "E2": "Economy Automatic",
    "F": "SUV",
    "G": "Luxury/Premium/Cabrio",
    "J1": "Crossover",
    "J2": "Station Wagon",
    "L1": "SUV Automatic",
    "L2": "Station Wagon Automatic",
    "M1": "7 Seater",
    "M2": "7 Seater Automatic",
    "N": "9 Seater/Minivan",
    "Others": "Others - Not Parameterized"
}

def analyze_vehicles_distribution():
    """Analisa a distribuição dos carros do VEHICLES por grupo"""
    print("=" * 100)
    print("ANÁLISE: Distribuição de Carros por Grupo (VEHICLES)")
    print("=" * 100)
    
    # Contar carros por grupo
    group_counts = defaultdict(list)
    
    for car_name, category in VEHICLES.items():
        group = map_category_to_group(category, car_name)
        group_counts[group].append((car_name, category))
    
    # Ordenar grupos por código
    sorted_groups = sorted(group_counts.keys())
    
    # Mostrar estatísticas
    total_cars = len(VEHICLES)
    print(f"\n📊 Total de carros no VEHICLES: {total_cars}\n")
    
    # Tabela de distribuição
    print(f"{'Código':<6} {'Nome do Grupo':<35} {'Quantidade':<12} {'%':<8}")
    print("-" * 100)
    
    for group in sorted_groups:
        cars = group_counts[group]
        count = len(cars)
        percentage = (count / total_cars) * 100
        group_name = GROUP_NAMES.get(group, group)
        print(f"{group:<6} {group_name:<35} {count:<12} {percentage:>6.1f}%")
    
    print("-" * 100)
    print(f"{'TOTAL':<6} {'':<35} {total_cars:<12} {'100.0%':>8}")
    
    # Mostrar detalhes de cada grupo
    print("\n" + "=" * 100)
    print("DETALHES POR GRUPO")
    print("=" * 100)
    
    for group in sorted_groups:
        cars = group_counts[group]
        count = len(cars)
        group_name = GROUP_NAMES.get(group, group)
        
        print(f"\n{group} - {group_name} ({count} carros):")
        print("-" * 100)
        
        # Mostrar até 20 carros por grupo (para não ficar muito longo)
        for i, (car, cat) in enumerate(sorted(cars), 1):
            if i <= 20:
                print(f"  {i:2}. {car:45} | Categoria: {cat}")
            elif i == 21:
                print(f"  ... e mais {count - 20} carros")
                break
    
    return group_counts

def analyze_common_categories():
    """Analisa categorias comuns do CarJet"""
    print("\n" + "=" * 100)
    print("ANÁLISE: Categorias Comuns do CarJet (Inglês)")
    print("=" * 100)
    
    # Categorias que o CarJet costuma retornar
    categories = [
        "Mini 4 Seats",
        "Mini 5 Seats",
        "Mini Automatic",
        "Economy",
        "Economy Automatic",
        "Compact",
        "SUV",
        "SUV Automatic",
        "Station Wagon",
        "Station Wagon Automatic",
        "Estate",
        "Crossover",
        "Luxury",
        "Premium",
        "Cabrio",
        "7 Seats",
        "7 Seater",
        "7 Seats Automatic",
        "People Carrier",
        "9 Seats",
        "9 Seater",
        "Minivan",
    ]
    
    print(f"\n{'Categoria (CarJet)':<35} {'Código':<10} {'Nome do Grupo':<35}")
    print("-" * 100)
    
    for cat in categories:
        group = map_category_to_group(cat, "")
        group_name = GROUP_NAMES.get(group, group)
        print(f"{cat:<35} {group:<10} {group_name:<35}")

def show_group_summary():
    """Mostra sumário visual dos grupos"""
    print("\n" + "=" * 100)
    print("📊 SUMÁRIO VISUAL - Distribuição por Grupo")
    print("=" * 100)
    
    # Analisar VEHICLES
    group_counts = defaultdict(int)
    for car_name, category in VEHICLES.items():
        group = map_category_to_group(category, car_name)
        group_counts[group] += 1
    
    total = len(VEHICLES)
    max_count = max(group_counts.values()) if group_counts else 1
    
    # Ordenar por quantidade (decrescente)
    sorted_groups = sorted(group_counts.items(), key=lambda x: x[1], reverse=True)
    
    print()
    for group, count in sorted_groups:
        group_name = GROUP_NAMES.get(group, group)
        percentage = (count / total) * 100
        bar_length = int((count / max_count) * 50)
        bar = "█" * bar_length
        
        print(f"{group:<6} {group_name:<35} {count:>4} ({percentage:>5.1f}%) {bar}")
    
    print()

def main():
    print("\n" + "🚗 " * 25)
    print("ANÁLISE COMPLETA: Distribuição de Carros por Grupo")
    print("🚗 " * 25 + "\n")
    
    # Análise 1: Distribuição dos VEHICLES
    group_counts = analyze_vehicles_distribution()
    
    # Análise 2: Categorias comuns do CarJet
    analyze_common_categories()
    
    # Sumário visual
    show_group_summary()
    
    # Estatísticas finais
    print("=" * 100)
    print("📈 ESTATÍSTICAS FINAIS")
    print("=" * 100)
    
    total_groups = len(group_counts)
    total_cars = len(VEHICLES)
    others_count = len(group_counts.get("Others", []))
    
    print(f"\nTotal de grupos utilizados: {total_groups}")
    print(f"Total de carros parametrizados: {total_cars}")
    print(f"Carros em 'Others': {others_count} ({(others_count/total_cars)*100:.1f}%)")
    print(f"Carros categorizados: {total_cars - others_count} ({((total_cars-others_count)/total_cars)*100:.1f}%)")
    
    # Grupo mais popular
    if group_counts:
        most_popular = max(group_counts.items(), key=lambda x: len(x[1]))
        group_code, cars = most_popular
        group_name = GROUP_NAMES.get(group_code, group_code)
        print(f"\nGrupo mais popular: {group_code} - {group_name} ({len(cars)} carros)")
    
    # Grupo menos popular (excluindo Others)
    non_others = {k: v for k, v in group_counts.items() if k != "Others"}
    if non_others:
        least_popular = min(non_others.items(), key=lambda x: len(x[1]))
        group_code, cars = least_popular
        group_name = GROUP_NAMES.get(group_code, group_code)
        print(f"Grupo menos popular: {group_code} - {group_name} ({len(cars)} carros)")
    
    print("\n" + "=" * 100)

if __name__ == "__main__":
    main()
