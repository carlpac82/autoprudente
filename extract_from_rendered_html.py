#!/usr/bin/env python3
"""
Extrai URLs de fotos REAIS diretamente do HTML renderizado pelo Selenium
Muito mais eficaz que tentar carregar lazy-load!
"""

import re
import json
import os
from bs4 import BeautifulSoup
from collections import defaultdict

def extract_photos_from_html(html_file, group_code):
    """Extrai fotos do HTML renderizado"""
    print(f"\n📄 A processar: {html_file}")
    
    with open(html_file, 'r', encoding='utf-8') as f:
        html = f.read()
    
    soup = BeautifulSoup(html, 'html.parser')
    
    cars = []
    seen_codes = set()
    
    # Procurar todos os <article>
    articles = soup.find_all('article', {'data-tab': 'car'})
    if not articles:
        articles = soup.find_all('article')
    
    print(f"  ✅ Encontrados {len(articles)} artigos")
    
    for idx, article in enumerate(articles, 1):
        try:
            # Nome do carro
            h2 = article.find('h2')
            if not h2:
                continue
            
            small = h2.find('small')
            if small:
                small.decompose()
            
            car_name = h2.get_text(strip=True)
            
            # Categoria
            cat_elem = article.find('span', class_='cl--name-type')
            category = cat_elem.get_text(strip=True) if cat_elem else 'Unknown'
            
            # Procurar TODAS as imagens no artigo
            imgs = article.find_all('img')
            
            photo_url = None
            car_code = None
            
            for img in imgs:
                # Tentar todos os atributos possíveis
                url = (
                    img.get('src') or
                    img.get('data-src') or
                    img.get('data-lazy') or
                    img.get('data-original')
                )
                
                if not url:
                    continue
                
                # Verificar se é foto de carro (não placeholder)
                if 'loading-car' in url:
                    continue
                
                # Extrair código
                match = re.search(r'/car_([A-Z0-9]+)\.(jpg|png|gif)', url)
                if match:
                    car_code = match.group(1)
                    
                    # Evitar duplicados
                    if car_code in seen_codes:
                        continue
                    
                    seen_codes.add(car_code)
                    
                    # Construir URL completa
                    if url.startswith('/'):
                        photo_url = 'https://www.carjet.com' + url
                    elif url.startswith('//'):
                        photo_url = 'https:' + url
                    else:
                        photo_url = url
                    
                    break
            
            if not photo_url or not car_code:
                continue
            
            # Parse variante
            variant = None
            variants = ['Cabrio', 'SW', 'Auto', 'Hybrid', 'Electric', '4x4', 'Gran Coupe', 'Coupe', 'Sedan']
            for v in variants:
                if re.search(rf',?\s*{re.escape(v)}$', car_name, re.IGNORECASE):
                    variant = v
                    break
            
            # Parse marca e modelo
            parts = car_name.split(' ', 1)
            brand = parts[0]
            model = parts[1] if len(parts) == 2 else ""
            
            if variant:
                model = model.replace(f", {variant}", "").replace(f" {variant}", "").strip()
            
            car_data = {
                'group': group_code,
                'index': idx,
                'name': car_name,
                'brand': brand,
                'model': model,
                'variant': variant,
                'category': category,
                'car_code': car_code,
                'photo_url': photo_url,
                'is_real': True  # Todas são reais!
            }
            
            cars.append(car_data)
            
            variant_info = f" [{variant}]" if variant else ""
            print(f"  ✅ {idx}. {car_name}{variant_info} (Código: {car_code})")
            
        except Exception as e:
            print(f"  ⚠️ Erro no artigo {idx}: {e}")
            continue
    
    return cars


def main():
    print("=" * 80)
    print("🔍 EXTRAÇÃO DE FOTOS DO HTML RENDERIZADO")
    print("=" * 80)
    
    # Procurar todos os HTMLs de grupos
    html_files = [f for f in os.listdir('.') if f.startswith('carjet_group_') and f.endswith('.html')]
    
    if not html_files:
        print("\n❌ Nenhum HTML encontrado!")
        print("Execute primeiro o download_by_groups.py")
        return
    
    print(f"\n📋 Encontrados {len(html_files)} ficheiros HTML")
    
    all_cars = []
    stats_by_group = {}
    
    for html_file in sorted(html_files):
        # Extrair código do grupo do nome do ficheiro
        # carjet_group_N.html -> N
        # carjet_group_B1_B2.html -> B1_B2
        group_code = html_file.replace('carjet_group_', '').replace('.html', '')
        
        cars = extract_photos_from_html(html_file, group_code)
        
        if cars:
            all_cars.extend(cars)
            stats_by_group[group_code] = len(cars)
            print(f"  📊 Grupo {group_code}: {len(cars)} fotos reais extraídas")
    
    if not all_cars:
        print("\n❌ Nenhuma foto extraída!")
        return
    
    # Guardar JSON
    json_file = 'carjet_cars_from_html.json'
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(all_cars, f, indent=2, ensure_ascii=False)
    
    print("\n" + "=" * 80)
    print("📊 ESTATÍSTICAS FINAIS")
    print("=" * 80)
    
    for group, count in sorted(stats_by_group.items()):
        print(f"Grupo {group}: {count} fotos reais")
    
    print(f"\n✅ Total: {len(all_cars)} fotos reais")
    print(f"💾 Guardado em: {json_file}")
    
    # Agrupar por código para ver duplicados
    by_code = defaultdict(list)
    for car in all_cars:
        by_code[car['car_code']].append(car)
    
    duplicates = {code: cars for code, cars in by_code.items() if len(cars) > 1}
    if duplicates:
        print(f"\n⚠️ {len(duplicates)} códigos duplicados encontrados")
        for code, cars in list(duplicates.items())[:5]:
            print(f"  {code}: {', '.join(c['name'] for c in cars)}")
    
    print("=" * 80)


if __name__ == '__main__':
    main()
