#!/usr/bin/env python3
"""
Script MELHORADO para extrair fotos da Carjet com garantia de mapeamento correto.
Usa o atributo ALT da imagem para identificação precisa.
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import requests
import os
import time
import re
import json

def extract_car_photos_precise(url):
    """
    Extrai fotos com mapeamento preciso usando ALT text
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
        
        # Scroll LENTO para carregar TODAS as imagens lazy-load
        print("📜 A fazer scroll LENTO para carregar todas as imagens...")
        
        # Obter altura total
        total_height = driver.execute_script("return document.body.scrollHeight")
        viewport_height = driver.execute_script("return window.innerHeight")
        
        # Scroll em incrementos pequenos
        current_position = 0
        scroll_increment = 300  # Scroll de 300px de cada vez
        
        while current_position < total_height:
            # Scroll para próxima posição
            driver.execute_script(f"window.scrollTo(0, {current_position});")
            time.sleep(1.5)  # Aguardar 1.5s para lazy-load carregar
            
            current_position += scroll_increment
            
            # Recalcular altura (pode ter aumentado)
            total_height = driver.execute_script("return document.body.scrollHeight")
        
        # Scroll até o final
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        
        # Voltar ao topo
        driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(1)
        
        print("✅ Scroll completo - todas as imagens devem estar carregadas")
        
        # Obter HTML completo
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        
        # Guardar HTML para debug
        with open('carjet_page_v2_debug.html', 'w', encoding='utf-8') as f:
            f.write(html)
        print("💾 HTML guardado em: carjet_page_v2_debug.html")
        
        # Procurar por elementos de carros
        print("\n🔎 A procurar elementos de carros...")
        
        # Estrutura da Carjet: <article data-tab="car">
        car_elements = soup.find_all('article', {'data-tab': 'car'})
        
        if not car_elements:
            car_elements = soup.find_all('article')
        
        print(f"  ✅ Encontrados {len(car_elements)} elementos <article>")
        print()
        
        # Processar cada carro
        for idx, car_elem in enumerate(car_elements, 1):
            try:
                # MÉTODO 1: Extrair do ALT da imagem (MAIS CONFIÁVEL)
                img_elem = car_elem.find('img', class_='cl--car-img')
                
                if not img_elem:
                    continue
                
                # Obter ALT text (ex: "Fiat Panda ou similar | Pequeno")
                alt_text = img_elem.get('alt', '')
                
                # Extrair nome e categoria do ALT
                car_name = None
                category = None
                
                if alt_text:
                    # Dividir por " | "
                    parts = alt_text.split('|')
                    
                    if len(parts) >= 1:
                        # Primeira parte contém nome (ex: "Fiat Panda ou similar")
                        name_part = parts[0].strip()
                        
                        # Remover "ou similar", "or similar", etc.
                        name_part = re.sub(r'\s+(ou|or|o)\s+similar.*$', '', name_part, flags=re.IGNORECASE)
                        car_name = name_part.strip()
                    
                    if len(parts) >= 2:
                        # Segunda parte contém categoria
                        category = parts[1].strip()
                
                # MÉTODO 2: Fallback para H2 se ALT não existir
                if not car_name:
                    name_div = car_elem.find('div', class_='cl--name')
                    if name_div:
                        h2 = name_div.find('h2')
                        if h2:
                            small = h2.find('small')
                            if small:
                                small.decompose()
                            car_name = h2.get_text(strip=True)
                    
                    # Categoria do span
                    if not category:
                        category_elem = car_elem.find('span', class_='cl--name-type')
                        if category_elem:
                            category = category_elem.get_text(strip=True)
                
                # Extrair URL da foto
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
                
                # Extrair código do carro da URL (ex: car_C45.jpg -> C45)
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
                if car_name and photo_url:
                    # Verificar se já existe (evitar duplicados)
                    existing = next((c for c in cars if c['name'] == car_name and c['photo_url'] == photo_url), None)
                    
                    if not existing:
                        car_data = {
                            'name': car_name,
                            'photo_url': photo_url,
                            'category': category or 'Unknown',
                            'car_code': car_code,
                            'is_placeholder': is_placeholder,
                            'alt_text': alt_text,
                            'index': idx
                        }
                        
                        cars.append(car_data)
                        
                        status = "⚠️ PLACEHOLDER" if is_placeholder else "✅"
                        print(f"{status} {idx}. {car_name}")
                        print(f"   Categoria: {category}")
                        print(f"   Código: {car_code}")
                        print(f"   URL: {photo_url}")
                        if alt_text:
                            print(f"   ALT: {alt_text}")
                        print()
                    
            except Exception as e:
                print(f"  ⚠️ Erro ao processar elemento {idx}: {e}")
                continue
        
        print(f"\n✅ Total de carros extraídos: {len(cars)}")
        
        # Estatísticas
        real_photos = sum(1 for c in cars if not c['is_placeholder'])
        placeholders = sum(1 for c in cars if c['is_placeholder'])
        
        print(f"   📸 Fotos reais: {real_photos}")
        print(f"   ⚠️ Placeholders: {placeholders}")
        
        # Guardar dados em JSON
        with open('carjet_cars_data_v2.json', 'w', encoding='utf-8') as f:
            json.dump(cars, f, indent=2, ensure_ascii=False)
        print("\n💾 Dados guardados em: carjet_cars_data_v2.json")
        
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


def download_photo(photo_url, car_name, car_code, output_dir='carjet_photos_v2'):
    """
    Faz download de uma foto de viatura
    """
    # Criar diretório se não existir
    os.makedirs(output_dir, exist_ok=True)
    
    # Nome do ficheiro baseado no código do carro (mais confiável)
    if car_code:
        # Usar código do carro como nome base
        safe_name = f"{car_code}_{car_name.replace(' ', '_').replace(',', '').replace('/', '_')}"
    else:
        # Fallback para nome do carro
        safe_name = car_name.replace(' ', '_').replace(',', '').replace('/', '_')
    
    # Limpar caracteres especiais
    safe_name = re.sub(r'[^\w\s-]', '', safe_name)
    
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
        
        # Verificar se é placeholder (< 1KB)
        if file_size < 1024:
            status = "⚠️ PLACEHOLDER"
        else:
            status = "✅"
        
        print(f"  {status} Download: {filename} ({file_size:,} bytes)")
        return filepath
        
    except Exception as e:
        print(f"  ❌ Erro ao fazer download de {car_name}: {e}")
        return None


def main():
    """Função principal"""
    
    # URL da página de resultados da Carjet
    url = "https://www.carjet.com/do/list/pt?s=c78a27c8-8d9d-4cc0-92bc-cdcce23a7b3b&b=22cb9498-751d-4517-9d49-a7d35f9945d3"
    
    print("=" * 80)
    print("🚗 DOWNLOAD DE FOTOS DA CARJET V2 (Mapeamento Preciso)")
    print("=" * 80)
    print()
    
    # Extrair dados dos carros
    cars = extract_car_photos_precise(url)
    
    if not cars:
        print("\n❌ Nenhum carro encontrado!")
        return
    
    print(f"\n📥 A fazer download de {len(cars)} fotos...")
    print()
    
    # Fazer download das fotos
    successful = 0
    failed = 0
    real_photos = 0
    placeholders = 0
    
    for idx, car in enumerate(cars, 1):
        print(f"[{idx}/{len(cars)}] {car['name']} (Código: {car['car_code']})")
        
        result = download_photo(car['photo_url'], car['name'], car['car_code'])
        
        if result:
            successful += 1
            if car['is_placeholder']:
                placeholders += 1
            else:
                real_photos += 1
        else:
            failed += 1
        
        # Delay entre downloads
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
    print(f"📁 Fotos guardadas em: carjet_photos_v2/")
    print("=" * 80)
    
    # Guardar lista de carros em ficheiro
    output_file = 'carjet_cars_list_v2.txt'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("LISTA DE CARROS EXTRAÍDOS DA CARJET (V2 - Mapeamento Preciso)\n")
        f.write("=" * 80 + "\n\n")
        
        for idx, car in enumerate(cars, 1):
            f.write(f"{idx}. {car['name']}\n")
            f.write(f"   Categoria: {car['category']}\n")
            f.write(f"   Código: {car['car_code']}\n")
            f.write(f"   URL Foto: {car['photo_url']}\n")
            f.write(f"   ALT Text: {car['alt_text']}\n")
            f.write(f"   Placeholder: {'Sim' if car['is_placeholder'] else 'Não'}\n")
            f.write("\n")
    
    print(f"📄 Lista de carros guardada em: {output_file}")
    
    # Criar relatório de fotos reais vs placeholders
    print("\n" + "=" * 80)
    print("📸 FOTOS REAIS ENCONTRADAS")
    print("=" * 80)
    
    real_cars = [c for c in cars if not c['is_placeholder']]
    if real_cars:
        for car in real_cars:
            print(f"✅ {car['name']} (Código: {car['car_code']})")
            print(f"   {car['photo_url']}")
    else:
        print("⚠️ Nenhuma foto real encontrada - todas são placeholders!")
    
    print("=" * 80)


if __name__ == '__main__':
    main()
