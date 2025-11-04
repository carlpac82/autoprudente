#!/usr/bin/env python3
"""
Extrai fotos e dados dos carros DIRETAMENTE do código fonte HTML da Carjet
SEM usar Selenium - muito mais rápido e confiável!
"""

import requests
import re
import json
from bs4 import BeautifulSoup

def extract_cars_from_html(url):
    """
    Extrai carros diretamente do HTML fonte
    """
    print(f"🔍 A fazer download do HTML de: {url}")
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'pt-PT,pt;q=0.9,en;q=0.8',
    }
    
    response = requests.get(url, headers=headers, timeout=30)
    response.raise_for_status()
    
    html = response.text
    
    # Guardar HTML para debug
    with open('carjet_html_source.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("💾 HTML guardado em: carjet_html_source.html")
    
    soup = BeautifulSoup(html, 'html.parser')
    
    cars = []
    
    # Procurar por <article> com data-tab="car"
    articles = soup.find_all('article', {'data-tab': 'car'})
    
    print(f"\n📦 Encontrados {len(articles)} artigos de carros")
    print()
    
    for idx, article in enumerate(articles, 1):
        try:
            # Extrair nome do H2
            h2 = article.find('h2')
            if not h2:
                continue
            
            # Remover <small>
            small = h2.find('small')
            if small:
                small.decompose()
            
            car_name = h2.get_text(strip=True)
            
            # Extrair categoria
            category_span = article.find('span', class_='cl--name-type')
            category = category_span.get_text(strip=True) if category_span else 'Unknown'
            
            # Extrair imagem
            img = article.find('img', class_='cl--car-img')
            if not img:
                continue
            
            # Tentar vários atributos
            photo_url = (
                img.get('src') or
                img.get('data-src') or
                img.get('data-lazy') or
                img.get('data-original')
            )
            
            if not photo_url:
                continue
            
            # Converter URL relativa
            if photo_url.startswith('/'):
                photo_url = 'https://www.carjet.com' + photo_url
            elif photo_url.startswith('//'):
                photo_url = 'https:' + photo_url
            
            # Extrair código do carro
            car_code = None
            match = re.search(r'/car_([A-Z0-9]+)\.(jpg|png|gif)', photo_url)
            if match:
                car_code = match.group(1)
            
            # Verificar se é placeholder
            is_placeholder = 'loading-car' in photo_url
            
            # Parse variante
            variant = None
            variants = ['Cabrio', 'SW', 'Auto', 'Hybrid', 'Electric', '4x4', 'Gran Coupe', 'Coupe', 'Sedan']
            
            for v in variants:
                if re.search(rf',?\s*{re.escape(v)}$', car_name, re.IGNORECASE):
                    variant = v
                    break
            
            car_data = {
                'index': idx,
                'name': car_name,
                'variant': variant,
                'category': category,
                'car_code': car_code,
                'photo_url': photo_url,
                'is_placeholder': is_placeholder
            }
            
            cars.append(car_data)
            
            status = "⚠️ PLACEHOLDER" if is_placeholder else "✅ REAL"
            variant_info = f" [{variant}]" if variant else ""
            
            print(f"{status} {idx}. {car_name}{variant_info}")
            print(f"   Código: {car_code}")
            print(f"   URL: {photo_url}")
            
        except Exception as e:
            print(f"❌ Erro no artigo {idx}: {e}")
            continue
    
    return cars


def main():
    url = "https://www.carjet.com/do/list/pt?s=c78a27c8-8d9d-4cc0-92bc-cdcce23a7b3b&b=22cb9498-751d-4517-9d49-a7d35f9945d3"
    
    print("=" * 80)
    print("🚗 EXTRAÇÃO DE FOTOS DO CÓDIGO FONTE HTML DA CARJET")
    print("=" * 80)
    print()
    
    cars = extract_cars_from_html(url)
    
    if not cars:
        print("\n❌ Nenhum carro encontrado!")
        return
    
    # Estatísticas
    real_photos = [c for c in cars if not c['is_placeholder']]
    placeholders = [c for c in cars if c['is_placeholder']]
    with_variants = [c for c in cars if c['variant']]
    
    print()
    print("=" * 80)
    print("📊 ESTATÍSTICAS")
    print("=" * 80)
    print(f"Total de carros: {len(cars)}")
    print(f"✅ Fotos reais: {len(real_photos)} ({len(real_photos)/len(cars)*100:.1f}%)")
    print(f"⚠️ Placeholders: {len(placeholders)} ({len(placeholders)/len(cars)*100:.1f}%)")
    print(f"🔄 Com variantes: {len(with_variants)}")
    print("=" * 80)
    
    # Guardar JSON
    with open('carjet_cars_from_source.json', 'w', encoding='utf-8') as f:
        json.dump(cars, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Dados guardados em: carjet_cars_from_source.json")
    
    # Listar fotos reais
    if real_photos:
        print("\n" + "=" * 80)
        print("📸 FOTOS REAIS ENCONTRADAS")
        print("=" * 80)
        for car in real_photos:
            variant_info = f" [{car['variant']}]" if car['variant'] else ""
            print(f"✅ {car['name']}{variant_info}")
            print(f"   Código: {car['car_code']}")
            print(f"   URL: {car['photo_url']}")
        print("=" * 80)
    
    # Listar variantes
    if with_variants:
        print("\n" + "=" * 80)
        print("🔄 VARIANTES ENCONTRADAS")
        print("=" * 80)
        
        # Agrupar por modelo base
        variants_by_model = {}
        for car in with_variants:
            base_name = car['name'].replace(f", {car['variant']}", "").replace(f" {car['variant']}", "")
            if base_name not in variants_by_model:
                variants_by_model[base_name] = []
            variants_by_model[base_name].append(car)
        
        for base_name, variants in sorted(variants_by_model.items()):
            print(f"\n{base_name}:")
            for v in variants:
                status = "✅" if not v['is_placeholder'] else "⚠️"
                print(f"  {status} {v['variant']} (Código: {v['car_code']})")
        
        print("=" * 80)


if __name__ == '__main__':
    main()
