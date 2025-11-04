#!/usr/bin/env python3
"""
Consolida fotos por GRUPO (não por carro)
Ignora duplicados mas mantém associação ao grupo do link
"""

import json
import os
from collections import defaultdict

# Mapeamento de grupos Carjet para categorias do sistema
GROUP_MAPPING = {
    'B1_B2': 'Mini',           # Mini/Económicos
    'N': 'Pequeno',            # Pequenos
    'C_D': 'Compacto',         # Compactos
    'M1': 'Médio',             # Médios
    'M2': 'Médio',             # Médios
    'E1_E2': 'Estate',         # Estate/SW
    'L1': 'Grande',            # Grandes
    'L2': 'Grande',            # Grandes
    'F_J1': 'SUV',             # SUVs/Familiares
    'J2': 'SUV',               # SUVs
    'G_X': 'Premium',          # Premium/Luxo
}

def consolidate_photos():
    """Consolida fotos mantendo grupo original"""
    
    print("=" * 80)
    print("🔄 CONSOLIDAÇÃO DE FOTOS POR GRUPO")
    print("=" * 80)
    
    # Carregar dados extraídos do HTML
    json_file = 'carjet_cars_from_html.json'
    
    if not os.path.exists(json_file):
        print(f"\n❌ Ficheiro não encontrado: {json_file}")
        return
    
    with open(json_file, 'r', encoding='utf-8') as f:
        all_cars = json.load(f)
    
    print(f"\n📊 Total de registos: {len(all_cars)}")
    
    # Agrupar por código (ignorar duplicados)
    unique_by_code = {}
    duplicates_info = defaultdict(list)
    
    for car in all_cars:
        code = car['car_code']
        group = car['group']
        
        if code not in unique_by_code:
            # Primeira ocorrência - guardar
            unique_by_code[code] = car
        else:
            # Duplicado - registar mas não guardar
            duplicates_info[code].append(group)
    
    print(f"✅ Códigos únicos: {len(unique_by_code)}")
    print(f"⚠️ Duplicados ignorados: {len(all_cars) - len(unique_by_code)}")
    
    # Organizar por grupo (do link original)
    by_group = defaultdict(list)
    
    for car in unique_by_code.values():
        group = car['group']
        
        # Adicionar categoria do sistema
        car['system_category'] = GROUP_MAPPING.get(group, 'Unknown')
        
        by_group[group].append(car)
    
    # Estatísticas por grupo
    print("\n" + "=" * 80)
    print("📊 FOTOS POR GRUPO (após remover duplicados)")
    print("=" * 80)
    
    for group in sorted(by_group.keys()):
        cars = by_group[group]
        category = GROUP_MAPPING.get(group, 'Unknown')
        print(f"{group:10} ({category:10}): {len(cars):2} fotos únicas")
    
    # Mostrar alguns duplicados
    if duplicates_info:
        print("\n" + "=" * 80)
        print("🔄 EXEMPLOS DE DUPLICADOS (mesmo carro em múltiplos grupos)")
        print("=" * 80)
        
        for code, groups in list(duplicates_info.items())[:10]:
            car = unique_by_code[code]
            original_group = car['group']
            duplicate_groups = ', '.join(groups)
            print(f"{code:6} {car['name']:30} | Original: {original_group:6} | Também em: {duplicate_groups}")
    
    # Guardar JSON consolidado
    consolidated_file = 'carjet_photos_consolidated.json'
    
    consolidated_data = {
        'by_group': {group: cars for group, cars in by_group.items()},
        'all_unique': list(unique_by_code.values()),
        'stats': {
            'total_unique': len(unique_by_code),
            'total_duplicates': len(all_cars) - len(unique_by_code),
            'by_group': {group: len(cars) for group, cars in by_group.items()}
        }
    }
    
    with open(consolidated_file, 'w', encoding='utf-8') as f:
        json.dump(consolidated_data, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Dados consolidados guardados em: {consolidated_file}")
    
    # Criar lista simples para importação
    import_list = []
    for car in unique_by_code.values():
        import_list.append({
            'car_code': car['car_code'],
            'name': car['name'],
            'brand': car['brand'],
            'model': car['model'],
            'variant': car['variant'],
            'group': car['group'],
            'category': car['system_category'],
            'photo_url': car['photo_url'],
            'photo_file': f"carjet_photos_real/{car['car_code']}_{car['brand']}_{car['model']}"
                         + (f"_{car['variant']}" if car['variant'] else "") + ".jpg"
        })
    
    import_file = 'carjet_photos_for_import.json'
    with open(import_file, 'w', encoding='utf-8') as f:
        json.dump(import_list, f, indent=2, ensure_ascii=False)
    
    print(f"💾 Lista para importação: {import_file}")
    
    print("\n" + "=" * 80)
    print("✅ CONSOLIDAÇÃO COMPLETA")
    print("=" * 80)
    print(f"Total de fotos únicas: {len(unique_by_code)}")
    print(f"Prontas para importar para BD")
    print("=" * 80)


if __name__ == '__main__':
    consolidate_photos()
