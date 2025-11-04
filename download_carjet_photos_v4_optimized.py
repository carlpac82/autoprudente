#!/usr/bin/env python3
"""
V4 OTIMIZADO - Scroll MUITO lento + Múltiplos passes para carregar TODAS as fotos reais
Objetivo: Aumentar taxa de fotos reais de 6.5% para 80%+
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
    """Separa marca, modelo e variante"""
    name = full_name.strip()
    
    variants = [
        'Cabrio', 'SW', 'Auto', 'Hybrid', 'Electric', '4x4',
        'Gran Coupe', 'Coupe', 'Sedan', 'Estate', 'Touring',
        '7 seater', '5 Door', 'Wagon'
    ]
    
    variant = None
    for v in variants:
        pattern_comma = rf',\s*{re.escape(v)}$'
        if re.search(pattern_comma, name, re.IGNORECASE):
            variant = v
            name = re.sub(pattern_comma, '', name, flags=re.IGNORECASE).strip()
            break
        
        pattern_space = rf'\s+{re.escape(v)}$'
        if re.search(pattern_space, name, re.IGNORECASE):
            variant = v
            name = re.sub(pattern_space, '', name, flags=re.IGNORECASE).strip()
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


def aggressive_lazy_load(driver):
    """
    Estratégia AGRESSIVA para carregar TODAS as imagens lazy-load
    
    Técnicas:
    1. Scroll MUITO lento (100px por vez, 3s delay)
    2. Múltiplos passes (3x up/down)
    3. Hover sobre cada imagem
    4. Aguardar carregamento de rede
    """
    print("📜 INICIANDO CARREGAMENTO AGRESSIVO DE IMAGENS...")
    print()
    
    # PASSE 1: Scroll lento para baixo
    print("🔽 PASSE 1: Scroll lento para BAIXO...")
    total_height = driver.execute_script("return document.body.scrollHeight")
    current_position = 0
    scroll_increment = 100  # Apenas 100px por vez!
    
    while current_position < total_height:
        driver.execute_script(f"window.scrollTo(0, {current_position});")
        
        # Aguardar 3 segundos para lazy-load
        time.sleep(3)
        
        # Verificar se altura mudou (conteúdo dinâmico)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height > total_height:
            total_height = new_height
        
        current_position += scroll_increment
        
        # Mostrar progresso
        progress = (current_position / total_height) * 100
        print(f"   Progresso: {progress:.1f}% ({current_position}/{total_height}px)", end='\r')
    
    print(f"\n   ✅ Chegou ao fim: {total_height}px")
    time.sleep(5)  # Aguardar 5s no final
    
    # PASSE 2: Scroll lento para cima
    print("\n🔼 PASSE 2: Scroll lento para CIMA...")
    while current_position > 0:
        current_position -= scroll_increment
        if current_position < 0:
            current_position = 0
        
        driver.execute_script(f"window.scrollTo(0, {current_position});")
        time.sleep(2)  # 2s no caminho de volta
        
        progress = ((total_height - current_position) / total_height) * 100
        print(f"   Progresso: {progress:.1f}%", end='\r')
    
    print(f"\n   ✅ Voltou ao topo")
    time.sleep(3)
    
    # PASSE 3: Scroll rápido até o meio e aguardar
    print("\n⏸️  PASSE 3: Aguardar no MEIO da página...")
    middle = total_height // 2
    driver.execute_script(f"window.scrollTo(0, {middle});")
    time.sleep(5)
    
    # PASSE 4: Hover sobre cada imagem de carro
    print("\n🖱️  PASSE 4: Hover sobre cada imagem...")
    driver.execute_script("window.scrollTo(0, 0);")
    time.sleep(2)
    
    try:
        images = driver.find_elements(By.CSS_SELECTOR, 'img.cl--car-img')
        print(f"   Encontradas {len(images)} imagens")
        
        for idx, img in enumerate(images, 1):
            try:
                # Scroll até a imagem
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", img)
                time.sleep(0.5)
                
                # Hover sobre a imagem
                driver.execute_script("""
                    var event = new MouseEvent('mouseover', {
                        'view': window,
                        'bubbles': true,
                        'cancelable': true
                    });
                    arguments[0].dispatchEvent(event);
                """, img)
                
                time.sleep(0.3)
                
                if idx % 10 == 0:
                    print(f"   Processadas {idx}/{len(images)} imagens", end='\r')
            except:
                continue
        
        print(f"\n   ✅ Hover completo em {len(images)} imagens")
    except Exception as e:
        print(f"   ⚠️ Erro no hover: {e}")
    
    # PASSE 5: Aguardar requisições de rede
    print("\n⏳ PASSE 5: Aguardar carregamento de rede...")
    time.sleep(5)
    
    # Voltar ao topo
    driver.execute_script("window.scrollTo(0, 0);")
    time.sleep(3)
    
    print("\n✅ CARREGAMENTO AGRESSIVO COMPLETO!")
    print()


def extract_car_photos_optimized(url):
    """Extrai fotos com carregamento otimizado"""
    print(f"🔍 A extrair dados de: {url}")
    
    # Configurar Chrome
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    # Desabilitar cache para forçar download de imagens
    chrome_options.add_argument('--disk-cache-size=0')
    chrome_options.add_argument('--media-cache-size=0')
    
    # User agent
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
        driver.set_page_load_timeout(60)
        
        print("📄 A carregar página...")
        driver.get(url)
        
        print("⏳ Aguardando carregamento inicial...")
        time.sleep(8)  # Aguardar mais tempo inicial
        
        # Rejeitar cookies
        try:
            cookie_buttons = driver.find_elements(By.XPATH, 
                "//button[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'rejeitar') or "
                "contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'recusar')]"
            )
            if cookie_buttons:
                cookie_buttons[0].click()
                print("🍪 Cookies rejeitados")
                time.sleep(2)
        except:
            pass
        
        # CARREGAMENTO AGRESSIVO
        aggressive_lazy_load(driver)
        
        # Obter HTML
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        
        # Guardar HTML
        with open('carjet_page_v4_debug.html', 'w', encoding='utf-8') as f:
            f.write(html)
        print("💾 HTML guardado em: carjet_page_v4_debug.html")
        
        # Extrair carros
        print("\n🔎 A extrair dados dos carros...")
        car_elements = soup.find_all('article', {'data-tab': 'car'})
        
        if not car_elements:
            car_elements = soup.find_all('article')
        
        print(f"  ✅ Encontrados {len(car_elements)} elementos")
        print()
        
        for idx, car_elem in enumerate(car_elements, 1):
            try:
                name_div = car_elem.find('div', class_='cl--name')
                if not name_div:
                    continue
                
                h2 = name_div.find('h2')
                if not h2:
                    continue
                
                small = h2.find('small')
                if small:
                    small.decompose()
                
                full_name = h2.get_text(strip=True)
                parsed = parse_car_name_with_variant(full_name)
                
                category_elem = car_elem.find('span', class_='cl--name-type')
                category = category_elem.get_text(strip=True) if category_elem else 'Unknown'
                
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
                
                if photo_url and not photo_url.startswith('http'):
                    if photo_url.startswith('//'):
                        photo_url = 'https:' + photo_url
                    elif photo_url.startswith('/'):
                        photo_url = 'https://www.carjet.com' + photo_url
                
                car_code = None
                if photo_url:
                    match = re.search(r'/car_([A-Z0-9]+)\.(jpg|png|gif|webp)', photo_url)
                    if match:
                        car_code = match.group(1)
                
                is_placeholder = False
                if photo_url and 'loading-car' in photo_url:
                    is_placeholder = True
                
                if full_name and photo_url:
                    unique_id = f"{car_code}_{full_name}" if car_code else full_name
                    
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
                            'category': category,
                            'car_code': car_code,
                            'is_placeholder': is_placeholder,
                            'index': idx
                        }
                        
                        cars.append(car_data)
                        
                        status = "⚠️ PLACEHOLDER" if is_placeholder else "✅ REAL"
                        variant_info = f" [{parsed['variant']}]" if parsed['variant'] else ""
                        
                        print(f"{status} {idx}. {parsed['brand']} {parsed['model']}{variant_info} (Código: {car_code})")
                    
            except Exception as e:
                print(f"  ⚠️ Erro no elemento {idx}: {e}")
                continue
        
        print(f"\n✅ Total extraído: {len(cars)}")
        
        # Estatísticas
        real_photos = sum(1 for c in cars if not c['is_placeholder'])
        placeholders = sum(1 for c in cars if c['is_placeholder'])
        with_variants = sum(1 for c in cars if c['variant'])
        
        print(f"   📸 Fotos reais: {real_photos} ({real_photos/len(cars)*100:.1f}%)")
        print(f"   ⚠️ Placeholders: {placeholders} ({placeholders/len(cars)*100:.1f}%)")
        print(f"   🔄 Variantes: {with_variants}")
        
        # Guardar JSON
        with open('carjet_cars_data_v4.json', 'w', encoding='utf-8') as f:
            json.dump(cars, f, indent=2, ensure_ascii=False)
        print("\n💾 Dados guardados em: carjet_cars_data_v4.json")
        
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


def download_photo(photo_url, car_data, output_dir='carjet_photos_v4'):
    """Download de foto"""
    os.makedirs(output_dir, exist_ok=True)
    
    car_code = car_data['car_code']
    brand = car_data['brand']
    model = car_data['model']
    variant = car_data['variant']
    
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
    
    safe_name = re.sub(r'[^\w\s-]', '', safe_name)
    
    ext = '.jpg'
    if '.' in photo_url:
        url_ext = photo_url.split('.')[-1].split('?')[0].lower()
        if url_ext in ['jpg', 'jpeg', 'png', 'webp', 'gif']:
            ext = f'.{url_ext}'
    
    filename = f"{safe_name}{ext}"
    filepath = os.path.join(output_dir, filename)
    
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
        status = "⚠️ PLACEHOLDER" if file_size < 1024 else "✅"
        
        print(f"  {status} Download: {filename} ({file_size:,} bytes)")
        return filepath
        
    except Exception as e:
        print(f"  ❌ Erro: {e}")
        return None


def main():
    url = "https://www.carjet.com/do/list/pt?s=c78a27c8-8d9d-4cc0-92bc-cdcce23a7b3b&b=22cb9498-751d-4517-9d49-a7d35f9945d3"
    
    print("=" * 80)
    print("🚗 DOWNLOAD V4 OTIMIZADO - Scroll Agressivo + Múltiplos Passes")
    print("=" * 80)
    print()
    
    cars = extract_car_photos_optimized(url)
    
    if not cars:
        print("\n❌ Nenhum carro encontrado!")
        return
    
    print(f"\n📥 A fazer download de {len(cars)} fotos...")
    print()
    
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
    print("📊 RESULTADO FINAL")
    print("=" * 80)
    print(f"✅ Downloads: {successful}")
    print(f"❌ Falhas: {failed}")
    print(f"📸 Fotos reais: {real_photos} ({real_photos/len(cars)*100:.1f}%)")
    print(f"⚠️ Placeholders: {placeholders} ({placeholders/len(cars)*100:.1f}%)")
    print(f"🎯 Melhoria: {real_photos/len(cars)*100 - 6.5:.1f}% vs V3")
    print(f"📁 Pasta: carjet_photos_v4/")
    print("=" * 80)


if __name__ == '__main__':
    main()
