#!/usr/bin/env python3
"""
Download de fotos da Carjet por GRUPOS específicos
Usando links diretos fornecidos pelo utilizador
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

# CONFIGURAÇÃO DOS GRUPOS
GROUPS = {
    'N': {
        'name': 'Grupo N',
        'url': 'https://www.carjet.com/do/list/pt?s=36b4f78e-2eb7-4ad3-b5ad-eefba5b8a662&b=b5feeaca-db6e-48d4-9fe3-c64d86ebe199',
        'description': 'Pequenos'
    },
    'M1': {
        'name': 'Grupo M1',
        'url': 'https://www.carjet.com/do/list/pt?s=f45d195b-911d-4eeb-9ff7-fb137fd67548&b=3d56041a-4a1f-4ed3-8fd7-450c9b71b134',
        'description': 'Médios 1'
    },
    'M2': {
        'name': 'Grupo M2',
        'url': 'https://www.carjet.com/do/list/pt?s=d197f989-6aae-42b5-88a7-61a31e63d3be&b=20d6e56b-c483-4fd6-9ebe-dbc0ed242ea8',
        'description': 'Médios 2'
    },
    'L1': {
        'name': 'Grupo L1',
        'url': 'https://www.carjet.com/do/list/pt?s=e36f74ac-d44a-4f4f-b212-776eb2e7cc74&b=ebbd9c0e-91bb-4ccc-8d5d-16b8c338a186',
        'description': 'Grandes 1'
    },
    'L2': {
        'name': 'Grupo L2',
        'url': 'https://www.carjet.com/do/list/pt?s=a02a4f13-a735-44f4-bb4a-d142bb424186&b=358c83df-5f3b-422a-a5e6-a5b0cb9d2d50',
        'description': 'Grandes 2'
    },
    'F_J1': {
        'name': 'Grupo F e J1',
        'url': 'https://www.carjet.com/do/list/pt?s=1c29e1ba-520f-48db-9e74-b793152c596d&b=d7fb5926-0c96-40b6-a4bb-420709565d97',
        'description': 'Familiares e SUVs 1'
    },
    'J2': {
        'name': 'Grupo J2',
        'url': 'https://www.carjet.com/do/list/pt?s=43f2520b-75ba-4a52-b849-e78fae23bcc9&b=98a47b70-ec71-45d3-8422-ba5dbdd5310d',
        'description': 'SUVs 2'
    },
    'B1_B2': {
        'name': 'Grupo B1 e B2',
        'url': 'https://www.carjet.com/do/list/pt?s=9885cac3-7593-4839-8da0-b763d8c5f91b&b=8f4c2c06-2a77-43bf-adcd-d744780aff6f',
        'description': 'Mini/Económicos'
    },
    'C_D': {
        'name': 'Grupo C e D',
        'url': 'https://www.carjet.com/do/list/pt?s=f66105ae-692c-4bc9-9761-1082df6aeeaf&b=1a58f60e-9e29-4450-83b1-7b4f556f9911',
        'description': 'Compactos e Intermédios'
    },
    'E1_E2': {
        'name': 'Grupo E1 e E2',
        'url': 'https://www.carjet.com/do/list/pt?s=0c939e90-8f0f-4b45-a7ff-ba3258dedf76&b=862d6fa4-dc5e-4392-881f-89ec17f82135',
        'description': 'Estate/SW'
    },
    'G_X': {
        'name': 'Grupo G e X',
        'url': 'https://www.carjet.com/do/list/pt?s=3aeff12c-13aa-4111-9bbd-2371f0decf43&b=72243663-5ac1-432a-9b3c-6f54b1db654b',
        'description': 'Premium/Luxo'
    },
}

def parse_car_name(full_name):
    """Parse nome do carro"""
    name = full_name.strip()
    
    variants = ['Cabrio', 'SW', 'Auto', 'Hybrid', 'Electric', '4x4', 'Gran Coupe', 'Coupe', 'Sedan']
    variant = None
    
    for v in variants:
        if re.search(rf',?\s*{re.escape(v)}$', name, re.IGNORECASE):
            variant = v
            name = re.sub(rf',?\s*{re.escape(v)}$', '', name, flags=re.IGNORECASE).strip()
            break
    
    parts = name.split(' ', 1)
    brand = parts[0]
    model = parts[1] if len(parts) == 2 else ""
    
    return {
        'brand': brand,
        'model': model,
        'variant': variant,
        'full_name': full_name,
        'base_name': name
    }


def extract_cars_from_group(url, group_code, group_name):
    """Extrai carros de um grupo específico"""
    print(f"\n{'='*80}")
    print(f"🔍 GRUPO {group_code}: {group_name}")
    print(f"{'='*80}")
    print(f"URL: {url}")
    print()
    
    # Configurar Chrome
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    
    user_agent = 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1'
    chrome_options.add_argument(f'user-agent={user_agent}')
    
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
        driver.set_page_load_timeout(60)
        
        print("📄 A carregar página...")
        driver.get(url)
        
        print("⏳ Aguardando...")
        time.sleep(8)
        
        # Rejeitar cookies
        try:
            cookie_buttons = driver.find_elements(By.XPATH, 
                "//button[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'rejeitar')]"
            )
            if cookie_buttons:
                cookie_buttons[0].click()
                print("🍪 Cookies rejeitados")
                time.sleep(2)
        except:
            pass
        
        # Scroll RÁPIDO (otimizado para links diretos)
        print("📜 A fazer scroll rápido...")
        total_height = driver.execute_script("return document.body.scrollHeight")
        current = 0
        increment = 300  # 300px por vez (2x mais rápido)
        
        while current < total_height:
            driver.execute_script(f"window.scrollTo(0, {current});")
            time.sleep(1.5)  # 1.5s delay (40% mais rápido)
            
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height > total_height:
                total_height = new_height
            
            current += increment
            progress = (current / total_height) * 100
            print(f"   Progresso: {progress:.1f}%", end='\r')
        
        print(f"\n   ✅ Scroll completo: {total_height}px")
        time.sleep(5)
        
        # Voltar ao topo
        driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(2)
        
        # Extrair HTML
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        
        # Guardar HTML
        html_file = f'carjet_group_{group_code}.html'
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"💾 HTML guardado: {html_file}")
        
        # Extrair carros
        print("\n🔎 A extrair carros...")
        articles = soup.find_all('article', {'data-tab': 'car'})
        
        if not articles:
            articles = soup.find_all('article')
        
        print(f"  ✅ Encontrados {len(articles)} artigos")
        print()
        
        for idx, article in enumerate(articles, 1):
            try:
                # Nome
                h2 = article.find('h2')
                if not h2:
                    continue
                
                small = h2.find('small')
                if small:
                    small.decompose()
                
                full_name = h2.get_text(strip=True)
                parsed = parse_car_name(full_name)
                
                # Categoria
                cat_elem = article.find('span', class_='cl--name-type')
                category = cat_elem.get_text(strip=True) if cat_elem else 'Unknown'
                
                # Imagem
                img = article.find('img', class_='cl--car-img')
                if not img:
                    continue
                
                photo_url = (
                    img.get('src') or
                    img.get('data-src') or
                    img.get('data-lazy')
                )
                
                if not photo_url:
                    continue
                
                if photo_url.startswith('/'):
                    photo_url = 'https://www.carjet.com' + photo_url
                elif photo_url.startswith('//'):
                    photo_url = 'https:' + photo_url
                
                # Código
                car_code = None
                match = re.search(r'/car_([A-Z0-9]+)\.(jpg|png|gif)', photo_url)
                if match:
                    car_code = match.group(1)
                
                is_placeholder = 'loading-car' in photo_url
                
                if full_name and photo_url:
                    car_data = {
                        'group': group_code,
                        'group_name': group_name,
                        'index': idx,
                        'name': full_name,
                        'brand': parsed['brand'],
                        'model': parsed['model'],
                        'variant': parsed['variant'],
                        'category': category,
                        'car_code': car_code,
                        'photo_url': photo_url,
                        'is_placeholder': is_placeholder
                    }
                    
                    cars.append(car_data)
                    
                    status = "⚠️" if is_placeholder else "✅"
                    variant_info = f" [{parsed['variant']}]" if parsed['variant'] else ""
                    
                    print(f"{status} {idx}. {full_name}{variant_info} (Código: {car_code})")
                    
            except Exception as e:
                print(f"  ⚠️ Erro no artigo {idx}: {e}")
                continue
        
        return cars
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        return []
        
    finally:
        if driver:
            driver.quit()
            print("🔒 Chrome fechado")


def download_photo(photo_url, car_data, base_dir='carjet_photos_by_group'):
    """Download de foto"""
    group_dir = os.path.join(base_dir, f"group_{car_data['group']}")
    os.makedirs(group_dir, exist_ok=True)
    
    car_code = car_data['car_code']
    brand = car_data['brand']
    model = car_data['model']
    variant = car_data['variant']
    
    if car_code:
        if variant:
            safe_name = f"{car_code}_{brand}_{model}_{variant}"
        else:
            safe_name = f"{car_code}_{brand}_{model}"
    else:
        if variant:
            safe_name = f"{brand}_{model}_{variant}"
        else:
            safe_name = f"{brand}_{model}"
    
    safe_name = safe_name.replace(' ', '_').replace(',', '')
    safe_name = re.sub(r'[^\w\s-]', '', safe_name)
    
    ext = '.jpg'
    if '.' in photo_url:
        url_ext = photo_url.split('.')[-1].split('?')[0].lower()
        if url_ext in ['jpg', 'jpeg', 'png', 'webp', 'gif']:
            ext = f'.{url_ext}'
    
    filename = f"{safe_name}{ext}"
    filepath = os.path.join(group_dir, filename)
    
    if os.path.exists(filepath):
        return filepath
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X)',
            'Referer': 'https://www.carjet.com/',
        }
        
        response = requests.get(photo_url, headers=headers, timeout=30)
        response.raise_for_status()
        
        with open(filepath, 'wb') as f:
            f.write(response.content)
        
        file_size = len(response.content)
        status = "⚠️" if file_size < 1024 else "✅"
        
        print(f"  {status} {filename} ({file_size:,} bytes)")
        return filepath
        
    except Exception as e:
        print(f"  ❌ Erro: {e}")
        return None


def main():
    print("=" * 80)
    print("🚗 DOWNLOAD DE FOTOS POR GRUPOS DA CARJET")
    print("=" * 80)
    
    all_cars = []
    
    # Processar cada grupo
    for group_code, group_info in GROUPS.items():
        cars = extract_cars_from_group(
            group_info['url'],
            group_code,
            group_info['name']
        )
        
        if cars:
            all_cars.extend(cars)
            
            # Estatísticas do grupo
            real = sum(1 for c in cars if not c['is_placeholder'])
            placeholders = len(cars) - real
            
            print(f"\n📊 GRUPO {group_code} - Estatísticas:")
            print(f"   Total: {len(cars)}")
            print(f"   ✅ Fotos reais: {real} ({real/len(cars)*100:.1f}%)")
            print(f"   ⚠️ Placeholders: {placeholders}")
            
            # Download das fotos
            print(f"\n📥 A fazer download do GRUPO {group_code}...")
            for idx, car in enumerate(cars, 1):
                variant_info = f" [{car['variant']}]" if car['variant'] else ""
                print(f"[{idx}/{len(cars)}] {car['name']}{variant_info}")
                download_photo(car['photo_url'], car)
                time.sleep(0.2)
    
    # Guardar JSON completo
    json_file = 'carjet_cars_by_groups.json'
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(all_cars, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Dados guardados: {json_file}")
    
    # Estatísticas globais
    print("\n" + "=" * 80)
    print("📊 ESTATÍSTICAS GLOBAIS")
    print("=" * 80)
    
    for group_code in GROUPS.keys():
        group_cars = [c for c in all_cars if c['group'] == group_code]
        if group_cars:
            real = sum(1 for c in group_cars if not c['is_placeholder'])
            print(f"Grupo {group_code}: {len(group_cars)} carros ({real} fotos reais)")
    
    print(f"\nTotal: {len(all_cars)} carros")
    print(f"Fotos reais: {sum(1 for c in all_cars if not c['is_placeholder'])}")
    print("=" * 80)


if __name__ == '__main__':
    main()
