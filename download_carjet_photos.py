#!/usr/bin/env python3
"""
Script para extrair links de fotos e nomes de viaturas da página de resultados da Carjet
e fazer download direto das imagens.
"""

import requests
from bs4 import BeautifulSoup
import os
import time
import re
from urllib.parse import urljoin

def extract_car_photos_from_carjet(url):
    """
    Extrai links de fotos e nomes de viaturas da página da Carjet
    
    Args:
        url: URL da página de resultados da Carjet
        
    Returns:
        Lista de dicionários com {name, photo_url, category}
    """
    print(f"🔍 A extrair dados de: {url}")
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'pt-PT,pt;q=0.9,en;q=0.8',
        'Referer': 'https://www.carjet.com/',
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        cars = []
        
        # Procurar por divs de carros - estrutura típica da Carjet
        # Tentar vários seletores possíveis
        car_elements = (
            soup.find_all('div', class_=re.compile(r'car-item|vehicle-item|result-item', re.I)) or
            soup.find_all('div', class_=re.compile(r'car|vehicle', re.I)) or
            soup.find_all('article') or
            soup.find_all('div', {'data-car': True}) or
            soup.find_all('div', {'data-vehicle': True})
        )
        
        print(f"📦 Encontrados {len(car_elements)} elementos de carros")
        
        for idx, car_elem in enumerate(car_elements, 1):
            try:
                # Extrair nome do carro
                name = None
                name_elem = (
                    car_elem.find('h2') or
                    car_elem.find('h3') or
                    car_elem.find('h4') or
                    car_elem.find(class_=re.compile(r'car-name|vehicle-name|model', re.I)) or
                    car_elem.find('span', class_=re.compile(r'name|title', re.I))
                )
                
                if name_elem:
                    name = name_elem.get_text(strip=True)
                
                # Extrair URL da foto
                photo_url = None
                img_elem = car_elem.find('img')
                
                if img_elem:
                    # Tentar vários atributos possíveis
                    photo_url = (
                        img_elem.get('src') or
                        img_elem.get('data-src') or
                        img_elem.get('data-lazy') or
                        img_elem.get('data-original')
                    )
                    
                    # Converter URL relativa para absoluta
                    if photo_url and not photo_url.startswith('http'):
                        photo_url = urljoin('https://www.carjet.com', photo_url)
                
                # Extrair categoria (se disponível)
                category = None
                category_elem = car_elem.find(class_=re.compile(r'category|group|class', re.I))
                if category_elem:
                    category = category_elem.get_text(strip=True)
                
                if name and photo_url:
                    cars.append({
                        'name': name,
                        'photo_url': photo_url,
                        'category': category or 'Unknown'
                    })
                    print(f"  ✅ {idx}. {name}")
                    
            except Exception as e:
                print(f"  ⚠️ Erro ao processar elemento {idx}: {e}")
                continue
        
        # Se não encontrou nada com os seletores acima, tentar procurar todas as imagens
        if not cars:
            print("⚠️ Nenhum carro encontrado com seletores padrão. A tentar extrair todas as imagens...")
            
            all_images = soup.find_all('img')
            for img in all_images:
                alt_text = img.get('alt', '')
                src = img.get('src') or img.get('data-src')
                
                # Filtrar imagens que parecem ser de carros
                if src and any(keyword in src.lower() for keyword in ['car', 'vehicle', 'auto', 'modelo']):
                    if not src.startswith('http'):
                        src = urljoin('https://www.carjet.com', src)
                    
                    cars.append({
                        'name': alt_text or f'Car_{len(cars)+1}',
                        'photo_url': src,
                        'category': 'Unknown'
                    })
        
        print(f"\n✅ Total de carros extraídos: {len(cars)}")
        return cars
        
    except Exception as e:
        print(f"❌ Erro ao extrair dados: {e}")
        return []


def download_photo(photo_url, car_name, output_dir='carjet_photos'):
    """
    Faz download de uma foto de viatura
    
    Args:
        photo_url: URL da foto
        car_name: Nome da viatura
        output_dir: Diretório de destino
        
    Returns:
        Caminho do ficheiro guardado ou None se falhar
    """
    # Criar diretório se não existir
    os.makedirs(output_dir, exist_ok=True)
    
    # Limpar nome do ficheiro
    safe_name = re.sub(r'[^\w\s-]', '', car_name).strip().replace(' ', '_')
    
    # Extrair extensão da URL
    ext = '.jpg'
    if '.' in photo_url:
        url_ext = photo_url.split('.')[-1].split('?')[0].lower()
        if url_ext in ['jpg', 'jpeg', 'png', 'webp', 'gif']:
            ext = f'.{url_ext}'
    
    filename = f"{safe_name}{ext}"
    filepath = os.path.join(output_dir, filename)
    
    # Se já existe, não fazer download novamente
    if os.path.exists(filepath):
        print(f"  ⏭️  Já existe: {filename}")
        return filepath
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15',
            'Referer': 'https://www.carjet.com/',
        }
        
        response = requests.get(photo_url, headers=headers, timeout=30, stream=True)
        response.raise_for_status()
        
        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        print(f"  ✅ Download: {filename} ({len(response.content)} bytes)")
        return filepath
        
    except Exception as e:
        print(f"  ❌ Erro ao fazer download de {car_name}: {e}")
        return None


def main():
    """Função principal"""
    
    # URL da página de resultados da Carjet
    url = "https://www.carjet.com/do/list/pt?s=c78a27c8-8d9d-4cc0-92bc-cdcce23a7b3b&b=22cb9498-751d-4517-9d49-a7d35f9945d3"
    
    print("=" * 80)
    print("🚗 DOWNLOAD DE FOTOS DE VIATURAS DA CARJET")
    print("=" * 80)
    print()
    
    # Extrair dados dos carros
    cars = extract_car_photos_from_carjet(url)
    
    if not cars:
        print("\n❌ Nenhum carro encontrado!")
        return
    
    print(f"\n📥 A fazer download de {len(cars)} fotos...")
    print()
    
    # Fazer download das fotos
    successful = 0
    failed = 0
    
    for idx, car in enumerate(cars, 1):
        print(f"[{idx}/{len(cars)}] {car['name']}")
        
        result = download_photo(car['photo_url'], car['name'])
        
        if result:
            successful += 1
        else:
            failed += 1
        
        # Delay entre downloads para não sobrecarregar o servidor
        if idx < len(cars):
            time.sleep(0.5)
    
    print()
    print("=" * 80)
    print(f"✅ Downloads bem-sucedidos: {successful}")
    print(f"❌ Downloads falhados: {failed}")
    print(f"📁 Fotos guardadas em: carjet_photos/")
    print("=" * 80)
    
    # Guardar lista de carros em ficheiro
    output_file = 'carjet_cars_list.txt'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("LISTA DE CARROS EXTRAÍDOS DA CARJET\n")
        f.write("=" * 80 + "\n\n")
        
        for idx, car in enumerate(cars, 1):
            f.write(f"{idx}. {car['name']}\n")
            f.write(f"   Categoria: {car['category']}\n")
            f.write(f"   URL Foto: {car['photo_url']}\n")
            f.write("\n")
    
    print(f"📄 Lista de carros guardada em: {output_file}")


if __name__ == '__main__':
    main()
