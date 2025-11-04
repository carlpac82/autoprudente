#!/usr/bin/env python3
"""
Script V3 - SUPORTE COMPLETO PARA VARIANTES
Trata cada variante como um carro único com foto própria.

Exemplos:
- Fiat 500 (C25) - Foto própria
- Fiat 500 Cabrio (GZ91) - Foto diferente
- VW Polo (C27) - Foto própria
- VW Polo Auto (outro código) - Foto diferente
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests
import os
import time
import re
import json

def parse_car_name_with_variant(full_name):
    """
    Separa marca, modelo e variante do nome completo
    
    Exemplos:
    - "Fiat 500" -> {brand: "Fiat", model: "500", variant: None}
    - "Fiat 500 Cabrio" -> {brand: "Fiat", model: "500", variant: "Cabrio"}
    - "VW Polo Auto" -> {brand: "VW", model: "Polo", variant: "Auto"}
    - "Mercedes E Class SW" -> {brand: "Mercedes", model: "E Class", variant: "SW"}
    """
    # Remover sufixos comuns do final
    name = full_name.strip()
    
    # Lista de variantes conhecidas
    variants = [
        'Cabrio', 'SW', 'Auto', 'Hybrid', 'Electric', '4x4',
        'Gran Coupe', 'Coupe', 'Sedan', 'Estate', 'Touring',
        '7 seater', '5 Door', 'Wagon'
    ]
    
    # Procurar variante no final do nome
    variant = None
    for v in variants:
        # Procurar com vírgula (ex: "Fiat 500, Hybrid")
        pattern_comma = rf',\s*{re.escape(v)}$'
        if re.search(pattern_comma, name, re.IGNORECASE):
            variant = v
            name = re.sub(pattern_comma, '', name, flags=re.IGNORECASE).strip()
            break
        
        # Procurar sem vírgula (ex: "Fiat 500 Cabrio")
        pattern_space = rf'\s+{re.escape(v)}$'
        if re.search(pattern_space, name, re.IGNORECASE):
            variant = v
            name = re.sub(pattern_space, '', name, flags=re.IGNORECASE).strip()
            break
    
    # Separar marca e modelo
    parts = name.split(' ', 1)
    
    if len(parts) == 2:
        brand = parts[0]
        model = parts[1]
    else:
        brand = parts[0]
        model = ""
    
    return {
        'brand': brand,
        'model': model,
        'variant': variant,
        'full_name': full_name,
        'base_name': name  # Nome sem variante
    }


def extract_car_photos_with_variants(url):
    """
    Extrai fotos identificando cada variante como carro único
    """
    print(f"🔍 A extrair dados de: {url}")
    
    # Configurar Chrome
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    # User agent mobile
    user_agent = 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1'
    chrome_options.add_argument(f'user-agent={user_agent}')
    
    # Mobile emulation
    mobile_emulation = {
        "deviceMetrics": {"width": 390, "height": 844, "pixelRatio": 3.0},
        "userAgent": user_agent
    }
    chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
    
    driver = None
    cars = []
    
    try:
        print("🌐 A abrir Chrome...")
        driver = webdriver.Chrome(options=chrome_options)
        driver.set_page_load_timeout(30)
        
        print("📄 A carregar página...")
        driver.get(url)
        
        # Aguardar carregamento
        print("⏳ A aguardar carregamento dos carros...")
        time.sleep(5)
        
        # Tentar rejeitar cookies
        try:
            cookie_buttons = driver.find_elements(By.XPATH, 
                "//button[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'rejeitar') or "
                "contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'recusar') or "
                "contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'reject')]"
            )
            if cookie_buttons:
                cookie_buttons[0].click()
                print("🍪 Cookies rejeitados")
                time.sleep(1)
        except:
            pass
        
        # Scroll MUITO LENTO para carregar TODAS as imagens
        print("📜 A fazer scroll MUITO LENTO para carregar todas as imagens...")
        
        total_height = driver.execute_script("return document.body.scrollHeight")
        current_position = 0
        scroll_increment = 200  # Scroll de 200px de cada vez
        
        while current_position < total_height:
            driver.execute_script(f"window.scrollTo(0, {current_position});")
            time.sleep(2)  # Aguardar 2s para lazy-load carregar
            
            current_position += scroll_increment
            total_height = driver.execute_script("return document.body.scrollHeight")
        
        # Scroll até o final
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)
        
        # Voltar ao topo
        driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(2)
        
        print("✅ Scroll completo - todas as imagens devem estar carregadas")
        
        # Obter HTML completo
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        
        # Guardar HTML para debug
        with open('carjet_page_v3_debug.html', 'w', encoding='utf-8') as f:
            f.write(html)
        print("💾 HTML guardado em: carjet_page_v3_debug.html")
        
        # Procurar por elementos de carros
        print("\n🔎 A procurar elementos de carros (incluindo variantes)...")
        
        car_elements = soup.find_all('article', {'data-tab': 'car'})
        
        if not car_elements:
            car_elements = soup.find_all('article')
        
        print(f"  ✅ Encontrados {len(car_elements)} elementos <article>")
        print()
        
        # Processar cada carro
        for idx, car_elem in enumerate(car_elements, 1):
            try:
                # Extrair nome do H2
                name_div = car_elem.find('div', class_='cl--name')
                if not name_div:
                    continue
                
                h2 = name_div.find('h2')
                if not h2:
                    continue
                
                # Remover <small>
                small = h2.find('small')
                if small:
                    small.decompose()
                
                full_name = h2.get_text(strip=True)
                
                # Parse nome com variante
                parsed = parse_car_name_with_variant(full_name)
                
                # Extrair categoria
                category = None
                category_elem = car_elem.find('span', class_='cl--name-type')
                if category_elem:
                    category = category_elem.get_text(strip=True)
                
                # Extrair foto
                img_elem = car_elem.find('img', class_='cl--car-img')
                if not img_elem:
                    continue
                
                photo_url = (
                    img_elem.get('src') or
                    img_elem.get('data-src') or
                    img_elem.get('data-lazy') or
                    img_elem.get('data-original') or
                    img_elem.get('data-srcset', '').split(',')[0].strip().split(' ')[0]
                )
                
                # Converter URL relativa para absoluta
                if photo_url and not photo_url.startswith('http'):
                    if photo_url.startswith('//'):
                        photo_url = 'https:' + photo_url
                    elif photo_url.startswith('/'):
                        photo_url = 'https://www.carjet.com' + photo_url
                
                # Extrair código do carro da URL
                car_code = None
                if photo_url:
                    match = re.search(r'/car_([A-Z0-9]+)\.(jpg|png|gif|webp)', photo_url)
                    if match:
                        car_code = match.group(1)
                
                # Verificar se é placeholder
                is_placeholder = False
                if photo_url and 'loading-car' in photo_url:
                    is_placeholder = True
                
                # Só adicionar se tiver nome e foto válida
                if full_name and photo_url:
                    # Criar identificador único: código + nome completo (com variante)
                    unique_id = f"{car_code}_{full_name}" if car_code else full_name
                    
                    # Verificar se já existe
                    existing = next((c for c in cars if c['unique_id'] == unique_id), None)
                    
                    if not existing:
                        car_data = {
                            'unique_id': unique_id,
                            'full_name': full_name,
                            'brand': parsed['brand'],
                            'model': parsed['model'],
                            'variant': parsed['variant'],
                            'base_name': parsed['base_name'],
                            'photo_url': photo_url,
                            'category': category or 'Unknown',
                            'car_code': car_code,
                            'is_placeholder': is_placeholder,
                            'index': idx
                        }
                        
                        cars.append(car_data)
                        
                        status = "⚠️ PLACEHOLDER" if is_placeholder else "✅"
                        variant_info = f" [{parsed['variant']}]" if parsed['variant'] else ""
                        
                        print(f"{status} {idx}. {parsed['brand']} {parsed['model']}{variant_info}")
                        print(f"   Código: {car_code}")
                        print(f"   Categoria: {category}")
                        print(f"   URL: {photo_url}")
                        print()
                    
            except Exception as e:
                print(f"  ⚠️ Erro ao processar elemento {idx}: {e}")
                continue
        
        print(f"\n✅ Total de carros extraídos: {len(cars)}")
        
        # Estatísticas
        real_photos = sum(1 for c in cars if not c['is_placeholder'])
        placeholders = sum(1 for c in cars if c['is_placeholder'])
        with_variants = sum(1 for c in cars if c['variant'])
        
        print(f"   📸 Fotos reais: {real_photos}")
        print(f"   ⚠️ Placeholders: {placeholders}")
        print(f"   🔄 Com variantes: {with_variants}")
        
        # Guardar dados em JSON
        with open('carjet_cars_data_v3.json', 'w', encoding='utf-8') as f:
            json.dump(cars, f, indent=2, ensure_ascii=False)
        print("\n💾 Dados guardados em: carjet_cars_data_v3.json")
        
        return cars
        
    except Exception as e:
        print(f"❌ Erro ao extrair dados: {e}")
        import traceback
        traceback.print_exc()
        return []
        
    finally:
        if driver:
            driver.quit()
            print("🔒 Chrome fechado")


def download_photo(photo_url, car_data, output_dir='carjet_photos_v3'):
    """
    Faz download de uma foto de viatura (incluindo variantes)
    """
    os.makedirs(output_dir, exist_ok=True)
    
    car_code = car_data['car_code']
    brand = car_data['brand']
    model = car_data['model']
    variant = car_data['variant']
    
    # Nome do ficheiro com variante
    if car_code:
        if variant:
            safe_name = f"{car_code}_{brand}_{model}_{variant}".replace(' ', '_').replace(',', '')
        else:
            safe_name = f"{car_code}_{brand}_{model}".replace(' ', '_').replace(',', '')
    else:
        if variant:
            safe_name = f"{brand}_{model}_{variant}".replace(' ', '_').replace(',', '')
        else:
            safe_name = f"{brand}_{model}".replace(' ', '_').replace(',', '')
    
    # Limpar caracteres especiais
    safe_name = re.sub(r'[^\w\s-]', '', safe_name)
    
    # Extrair extensão
    ext = '.jpg'
    if '.' in photo_url:
        url_ext = photo_url.split('.')[-1].split('?')[0].lower()
        if url_ext in ['jpg', 'jpeg', 'png', 'webp', 'gif']:
            ext = f'.{url_ext}'
    
    filename = f"{safe_name}{ext}"
    filepath = os.path.join(output_dir, filename)
    
    # Se já existe
    if os.path.exists(filepath):
        file_size = os.path.getsize(filepath)
        print(f"  ⏭️  Já existe: {filename} ({file_size:,} bytes)")
        return filepath
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15',
            'Referer': 'https://www.carjet.com/',
        }
        
        response = requests.get(photo_url, headers=headers, timeout=30)
        response.raise_for_status()
        
        with open(filepath, 'wb') as f:
            f.write(response.content)
        
        file_size = len(response.content)
        
        # Verificar se é placeholder
        if file_size < 1024:
            status = "⚠️ PLACEHOLDER"
        else:
            status = "✅"
        
        print(f"  {status} Download: {filename} ({file_size:,} bytes)")
        return filepath
        
    except Exception as e:
        print(f"  ❌ Erro ao fazer download: {e}")
        return None


def main():
    """Função principal"""
    
    url = "https://www.carjet.com/do/list/pt?s=c78a27c8-8d9d-4cc0-92bc-cdcce23a7b3b&b=22cb9498-751d-4517-9d49-a7d35f9945d3"
    
    print("=" * 80)
    print("🚗 DOWNLOAD DE FOTOS DA CARJET V3 (Suporte para Variantes)")
    print("=" * 80)
    print()
    
    # Extrair dados
    cars = extract_car_photos_with_variants(url)
    
    if not cars:
        print("\n❌ Nenhum carro encontrado!")
        return
    
    print(f"\n📥 A fazer download de {len(cars)} fotos...")
    print()
    
    # Fazer download
    successful = 0
    failed = 0
    real_photos = 0
    placeholders = 0
    
    for idx, car in enumerate(cars, 1):
        variant_info = f" [{car['variant']}]" if car['variant'] else ""
        print(f"[{idx}/{len(cars)}] {car['brand']} {car['model']}{variant_info} (Código: {car['car_code']})")
        
        result = download_photo(car['photo_url'], car)
        
        if result:
            successful += 1
            if car['is_placeholder']:
                placeholders += 1
            else:
                real_photos += 1
        else:
            failed += 1
        
        if idx < len(cars):
            time.sleep(0.3)
    
    print()
    print("=" * 80)
    print("📊 ESTATÍSTICAS FINAIS")
    print("=" * 80)
    print(f"✅ Downloads bem-sucedidos: {successful}")
    print(f"❌ Downloads falhados: {failed}")
    print(f"📸 Fotos reais (> 1KB): {real_photos}")
    print(f"⚠️ Placeholders (< 1KB): {placeholders}")
    print(f"🔄 Com variantes: {sum(1 for c in cars if c['variant'])}")
    print(f"📁 Fotos guardadas em: carjet_photos_v3/")
    print("=" * 80)
    
    # Listar variantes encontradas
    print("\n" + "=" * 80)
    print("🔄 VARIANTES ENCONTRADAS")
    print("=" * 80)
    
    variants_found = {}
    for car in cars:
        if car['variant']:
            base = f"{car['brand']} {car['model']}"
            if base not in variants_found:
                variants_found[base] = []
            variants_found[base].append({
                'variant': car['variant'],
                'code': car['car_code'],
                'url': car['photo_url'],
                'is_real': not car['is_placeholder']
            })
    
    if variants_found:
        for base_name, variants in sorted(variants_found.items()):
            print(f"\n{base_name}:")
            for v in variants:
                status = "✅" if v['is_real'] else "⚠️"
                print(f"  {status} {v['variant']} (Código: {v['code']})")
                print(f"     {v['url']}")
    else:
        print("Nenhuma variante encontrada.")
    
    print("=" * 80)


if __name__ == '__main__':
    main()
