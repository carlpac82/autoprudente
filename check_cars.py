#!/usr/bin/env python3
"""Script para verificar carros reais da CarJet"""

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

def is_auto_from_name(name: str) -> bool:
    """Detecta se é automático pelo nome"""
    patterns = [
        r'\bauto\b',
        r'\bautomatic\b',
        r'\bautomático\b',
        r'\belectric\b',
        r'\be-\d+',
    ]
    return any(re.search(p, name.lower()) for p in patterns)

def find_in_vehicles(name: str):
    """Procura no VEHICLES"""
    norm = normalize_name(name)
    
    # Match exato
    if norm in VEHICLES:
        cat = VEHICLES[norm]
        return cat, ('Auto' in cat)
    
    # Variações
    variations = [
        norm.replace('volkswagen', 'vw'),
        norm.replace('vw', 'volkswagen'),
        norm.replace('citroën', 'citroen'),
    ]
    for v in variations:
        if v in VEHICLES:
            cat = VEHICLES[v]
            return cat, ('Auto' in cat)
    
    # Busca parcial
    for k in sorted(VEHICLES.keys(), key=len, reverse=True):
        if k in norm or norm in k:
            cat = VEHICLES[k]
            return cat, ('Auto' in cat)
    
    return None, None

def main():
    print("\n🚗 VERIFICAÇÃO DE CARROS - CarJet Direct API\n")
    
    # Fazer scraping
    location = "Faro, Aeroporto de Faro (FAO)"
    start_date = datetime.now() + timedelta(days=7)
    end_date = start_date + timedelta(days=7)
    
    print(f"📍 Local: {location}")
    print(f"📅 Datas: {start_date.strftime('%d/%m/%Y')} → {end_date.strftime('%d/%m/%Y')}\n")
    print("⏳ Fazendo scraping...\n")
    
    cars = scrape_carjet_direct(location, start_date, end_date)
    
    print(f"✅ {len(cars)} carros encontrados\n")
    print("="*80)
    print("ANÁLISE DE TRANSMISSÕES")
    print("="*80 + "\n")
    
    # Agrupar por transmissão
    autos_by_name = []
    manuals_by_name = []
    unknown = []
    
    for car in cars:
        name = car.get('car', '')
        if not name:
            continue
        
        is_auto_name = is_auto_from_name(name)
        cat, is_auto_dict = find_in_vehicles(name)
        
        if is_auto_name:
            autos_by_name.append({'name': name, 'cat': cat, 'in_dict': is_auto_dict})
        else:
            manuals_by_name.append({'name': name, 'cat': cat, 'in_dict': is_auto_dict})
    
    # Mostrar automáticos
    print(f"🔷 AUTOMÁTICOS (pelo nome) - {len(autos_by_name)} carros\n")
    for car in autos_by_name[:20]:
        status = "✅" if car['in_dict'] is True else "❌" if car['in_dict'] is False else "❓"
        print(f"{status} {car['name'][:60]:<60} → {car['cat'] if car['cat'] else 'NÃO ENCONTRADO'}")
    
    if len(autos_by_name) > 20:
        print(f"\n... e mais {len(autos_by_name) - 20} carros\n")
    
    # Mostrar manuais
    print(f"\n🔷 MANUAIS (provável) - {len(manuals_by_name)} carros\n")
    for car in manuals_by_name[:20]:
        status = "✅" if car['in_dict'] is False else "❌" if car['in_dict'] is True else "❓"
        print(f"{status} {car['name'][:60]:<60} → {car['cat'] if car['cat'] else 'NÃO ENCONTRADO'}")
    
    if len(manuals_by_name) > 20:
        print(f"\n... e mais {len(manuals_by_name) - 20} carros\n")
    
    # Procurar problemas
    print(f"\n{'='*80}")
    print("PROBLEMAS POTENCIAIS")
    print("="*80 + "\n")
    
    problems = []
    
    # Automáticos marcados como manuais
    for car in autos_by_name:
        if car['in_dict'] is False:
            problems.append({
                'name': car['name'],
                'issue': 'AUTO no nome mas MANUAL no dict',
                'cat': car['cat']
            })
    
    # Manuais marcados como automáticos
    for car in manuals_by_name:
        if car['in_dict'] is True:
            problems.append({
                'name': car['name'],
                'issue': 'Sem AUTO no nome mas AUTO no dict',
                'cat': car['cat']
            })
    
    if problems:
        for p in problems:
            print(f"❌ {p['name']}")
            print(f"   {p['issue']}")
            print(f"   Categoria: {p['cat']}\n")
    else:
        print("✅ Nenhum problema óbvio detectado!\n")
    
    print(f"{'='*80}")
    print(f"📊 RESUMO:")
    print(f"   - Total de carros: {len(cars)}")
    print(f"   - Automáticos (pelo nome): {len(autos_by_name)}")
    print(f"   - Manuais (provável): {len(manuals_by_name)}")
    print(f"   - Problemas detectados: {len(problems)}")
    print(f"{'='*80}\n")

if __name__ == "__main__":
    main()
