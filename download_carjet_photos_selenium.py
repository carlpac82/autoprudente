#!/usr/bin/env python3
"""
Script para extrair links de fotos e nomes de viaturas da página de resultados da Carjet
usando Selenium (para páginas com JavaScript) e fazer download direto das imagens.
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

def extract_car_photos_with_selenium(url):
    """
    Extrai links de fotos e nomes de viaturas da página da Carjet usando Selenium
    
    Args:
        url: URL da página de resultados da Carjet
        
    Returns:
        Lista de dicionários com {name, photo_url, category}
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
        
        # Tentar rejeitar cookies se aparecer
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
        
        # Scroll para carregar todas as imagens lazy-load
        print("📜 A fazer scroll para carregar imagens...")
        last_height = driver.execute_script("return document.body.scrollHeight")
        
        for _ in range(5):  # Scroll 5 vezes
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
        
        # Voltar ao topo
        driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(1)
        
        # Obter HTML completo
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        
        # Guardar HTML para debug
        with open('carjet_page_debug.html', 'w', encoding='utf-8') as f:
            f.write(html)
        print("💾 HTML guardado em: carjet_page_debug.html")
        
        # Procurar por elementos de carros - estrutura específica da Carjet
        print("\n🔎 A procurar elementos de carros...")
        
        # Estrutura da Carjet: <article> com classe que contém "car" ou "discount"
        car_elements = soup.find_all('article', {'data-tab': 'car'})
        
        if not car_elements:
            # Fallback: procurar todos os articles
            car_elements = soup.find_all('article')
        
        print(f"  ✅ Encontrados {len(car_elements)} elementos <article>")
        
        # Processar elementos de carros encontrados
        for idx, car_elem in enumerate(car_elements, 1):
            try:
                # Extrair nome do carro
                # Estrutura: <div class="cl--name"><h2>Nome do Carro <small>ou similar</small></h2>
                name = None
                name_div = car_elem.find('div', class_='cl--name')
                if name_div:
                    h2 = name_div.find('h2')
                    if h2:
                        # Remover o <small> se existir
                        small = h2.find('small')
                        if small:
                            small.decompose()
                        name = h2.get_text(strip=True)
                
                # Extrair foto do carro
                # Estrutura: <img class="cl--car-img" src="/cdn/img/cars/L/car_XXX.jpg">
                photo_url = None
                img_elem = car_elem.find('img', class_='cl--car-img')
                
                if img_elem:
                    photo_url = (
                        img_elem.get('src') or
                        img_elem.get('data-src') or
                        img_elem.get('data-lazy') or
                        img_elem.get('data-original')
                    )
                    
                    # Converter URL relativa para absoluta
                    if photo_url and not photo_url.startswith('http'):
                        if photo_url.startswith('//'):
                            photo_url = 'https:' + photo_url
                        elif photo_url.startswith('/'):
                            photo_url = 'https://www.carjet.com' + photo_url
                
                # Extrair categoria/tipo
                # Estrutura: <span class="cl--name-type">Pequeno</span>
                category = None
                category_elem = car_elem.find('span', class_='cl--name-type')
                if category_elem:
                    category = category_elem.get_text(strip=True)
                
                # Só adicionar se tiver nome e foto
                if name and photo_url:
                    # Verificar se já existe (evitar duplicados)
                    if not any(c['name'] == name and c['photo_url'] == photo_url for c in cars):
                        cars.append({
                            'name': name,
                            'photo_url': photo_url,
                            'category': category or 'Unknown'
                        })
                        print(f"  ✅ {idx}. {name} ({category or 'Unknown'})")
                    
            except Exception as e:
                print(f"  ⚠️ Erro ao processar elemento {idx}: {e}")
                continue
        
        print(f"\n✅ Total de carros extraídos: {len(cars)}")
        
        # Guardar dados em JSON
        with open('carjet_cars_data.json', 'w', encoding='utf-8') as f:
            json.dump(cars, f, indent=2, ensure_ascii=False)
        print("💾 Dados guardados em: carjet_cars_data.json")
        
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
        
        response = requests.get(photo_url, headers=headers, timeout=30)
        response.raise_for_status()
        
        with open(filepath, 'wb') as f:
            f.write(response.content)
        
        file_size = len(response.content)
        print(f"  ✅ Download: {filename} ({file_size:,} bytes)")
        return filepath
        
    except Exception as e:
        print(f"  ❌ Erro ao fazer download de {car_name}: {e}")
        return None


def main():
    """Função principal"""
    
    # URL da página de resultados da Carjet
    url = "https://www.carjet.com/do/list/pt?s=c78a27c8-8d9d-4cc0-92bc-cdcce23a7b3b&b=22cb9498-751d-4517-9d49-a7d35f9945d3"
    
    print("=" * 80)
    print("🚗 DOWNLOAD DE FOTOS DE VIATURAS DA CARJET (com Selenium)")
    print("=" * 80)
    print()
    
    # Extrair dados dos carros
    cars = extract_car_photos_with_selenium(url)
    
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
        
        # Delay entre downloads
        if idx < len(cars):
            time.sleep(0.3)
    
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
