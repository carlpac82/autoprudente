#!/usr/bin/env python3
"""
Teste: ROTAÇÃO COMPLETA - 7 IDIOMAS
"""
import sys
import time
import random
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

print("=" * 80, flush=True)
print("TESTE - ROTAÇÃO 7 IDIOMAS", flush=True)
print("=" * 80, flush=True)

# ============================================
# ROTAÇÃO COMPLETA - 7 IDIOMAS
# ============================================
languages = [
    {
        'name': '🇵🇹 Português',
        'url': 'https://www.carjet.com/aluguel-carros/index.htm',
        'locations': ['Faro Aeroporto (FAO)', 'Albufeira Cidade']
    },
    {
        'name': '🇬🇧 English',
        'url': 'https://www.carjet.com/index.htm',
        'locations': ['Faro Airport (FAO)', 'Albufeira City']
    },
    {
        'name': '🇫🇷 Français',
        'url': 'https://www.carjet.com/location-voitures/index.htm',
        'locations': ['Faro Aéroport (FAO)', 'Albufeira Centre ville']
    },
    {
        'name': '🇪🇸 Español',
        'url': 'https://www.carjet.com/alquiler-coches/index.htm',
        'locations': ['Faro Aeropuerto (FAO)', 'Albufeira Ciudad']
    },
    {
        'name': '🇩🇪 Deutsch',
        'url': 'https://www.carjet.com/mietwagen/index.htm',
        'locations': ['Faro Flughafen (FAO)', 'Albufeira Stadt']
    },
    {
        'name': '🇮🇹 Italiano',
        'url': 'https://www.carjet.com/autonoleggio/index.htm',
        'locations': ['Faro Aeroporto (FAO)', 'Albufeira Città']
    },
    {
        'name': '🇳🇱 Nederlands',
        'url': 'https://www.carjet.com/autohuur/index.htm',
        'locations': ['Faro Vliegveld (FAO)', 'Albufeira Stad']
    }
]

# Selecionar idioma e local aleatoriamente
selected_lang = random.choice(languages)
selected_location = random.choice(selected_lang['locations'])

# Datas
start_dt = datetime.now() + timedelta(days=7)
end_dt = start_dt + timedelta(days=5)

# Rotação de horas
available_hours = ['14:30', '15:00', '15:30', '16:00', '16:30', '17:00']
selected_hour = random.choice(available_hours)

# Rotação de dispositivos
mobile_devices = [
    {
        'name': 'iPhone 13',
        'ua': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1',
        'width': 390, 'height': 844, 'pixelRatio': 3.0
    },
    {
        'name': 'iPhone 12',
        'ua': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1',
        'width': 390, 'height': 844, 'pixelRatio': 3.0
    },
    {
        'name': 'Samsung Galaxy S21',
        'ua': 'Mozilla/5.0 (Linux; Android 12; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Mobile Safari/537.36',
        'width': 360, 'height': 800, 'pixelRatio': 3.0
    },
    {
        'name': 'Google Pixel 5',
        'ua': 'Mozilla/5.0 (Linux; Android 11; Pixel 5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Mobile Safari/537.36',
        'width': 393, 'height': 851, 'pixelRatio': 2.75
    }
]

selected_device = random.choice(mobile_devices)

print(f"\n📋 Parâmetros ALEATÓRIOS:", flush=True)
print(f"   Idioma: {selected_lang['name']}", flush=True)
print(f"   URL: {selected_lang['url']}", flush=True)
print(f"   Local: {selected_location}", flush=True)
print(f"   Datas: {start_dt.strftime('%d/%m/%Y')} - {end_dt.strftime('%d/%m/%Y')}", flush=True)
print(f"   Hora: {selected_hour}", flush=True)
print(f"   Device: {selected_device['name']}", flush=True)
print(f"\n🎲 Total de combinações possíveis: 7 idiomas × 2 locais × 6 horas × 4 devices = 336 variações!", flush=True)

chrome_options = Options()
chrome_options.add_argument('--start-maximized')  # VISÍVEL!
chrome_options.add_argument(f'user-agent={selected_device["ua"]}')

mobile_emulation = {
    "deviceMetrics": { 
        "width": selected_device['width'], 
        "height": selected_device['height'], 
        "pixelRatio": selected_device['pixelRatio']
    },
    "userAgent": selected_device['ua']
}
chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)

print("\n🚀 Iniciando Chrome VISÍVEL...", flush=True)
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

try:
    print(f"\n1️⃣  Abrindo site {selected_lang['name']}...", flush=True)
    driver.get(selected_lang['url'])
    time.sleep(2)
    
    print("\n2️⃣  Removendo cookies...", flush=True)
    driver.execute_script("document.querySelectorAll('[id*=cookie], [class*=cookie]').forEach(el => el.remove());")
    time.sleep(1)
    
    print(f"\n3️⃣  Preenchendo local: {selected_location}...", flush=True)
    pickup = driver.find_element(By.ID, "pickup")
    pickup.clear()
    pickup.send_keys(selected_location)
    print("   ✅ Digitado", flush=True)
    time.sleep(2)
    
    print("\n4️⃣  Clicando no dropdown...", flush=True)
    try:
        dropdown_selector = f"#recogida_lista li[data-id='{selected_location}']"
        dropdown_item = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, dropdown_selector))
        )
        dropdown_item.click()
        print(f"   ✅ '{selected_location}' selecionado", flush=True)
    except:
        try:
            driver.execute_script(f"document.querySelector('#recogida_lista li[data-id=\"{selected_location}\"]').click();")
            print(f"   ✅ Selecionado via JS", flush=True)
        except:
            print("   ⚠️  Dropdown não encontrado", flush=True)
    
    time.sleep(2)
    
    print("\n5️⃣  Preenchendo datas...", flush=True)
    driver.execute_script("""
        const fechaRec = document.querySelector('input[id="fechaRecogida"]');
        if (fechaRec) {
            fechaRec.value = arguments[0];
            fechaRec.dispatchEvent(new Event('input', {bubbles: true}));
            fechaRec.dispatchEvent(new Event('change', {bubbles: true}));
        }
    """, start_dt.strftime("%d/%m/%Y"))
    print(f"   ✅ Data recolha: {start_dt.strftime('%d/%m/%Y')}", flush=True)
    time.sleep(0.5)
    
    driver.execute_script("""
        const fechaDev = document.querySelector('input[id="fechaDevolucion"]');
        if (fechaDev) {
            fechaDev.value = arguments[0];
            fechaDev.dispatchEvent(new Event('input', {bubbles: true}));
            fechaDev.dispatchEvent(new Event('change', {bubbles: true}));
        }
    """, end_dt.strftime("%d/%m/%Y"))
    print(f"   ✅ Data devolução: {end_dt.strftime('%d/%m/%Y')}", flush=True)
    time.sleep(0.5)
    
    print(f"\n6️⃣  Preenchendo horas: {selected_hour}...", flush=True)
    driver.execute_script("""
        const horaRec = document.querySelector('select[id="fechaRecogidaSelHour"]');
        const horaDev = document.querySelector('select[id="fechaDevolucionSelHour"]');
        if (horaRec) {
            horaRec.value = arguments[0];
            horaRec.dispatchEvent(new Event('change', {bubbles: true}));
        }
        if (horaDev) {
            horaDev.value = arguments[0];
            horaDev.dispatchEvent(new Event('change', {bubbles: true}));
        }
    """, selected_hour)
    print(f"   ✅ Horas: {selected_hour}", flush=True)
    time.sleep(1)
    
    print("\n7️⃣  Verificando valores...", flush=True)
    values = driver.execute_script("""
        return {
            pickup: document.querySelector('input[id="pickup"]')?.value || 'VAZIO',
            fechaRecogida: document.querySelector('input[id="fechaRecogida"]')?.value || 'VAZIO',
            fechaDevolucion: document.querySelector('input[id="fechaDevolucion"]')?.value || 'VAZIO',
            horaRecogida: document.querySelector('select[id="fechaRecogidaSelHour"]')?.value || 'VAZIO',
            horaDevolucion: document.querySelector('select[id="fechaDevolucionSelHour"]')?.value || 'VAZIO'
        };
    """)
    
    all_ok = True
    for key, val in values.items():
        if val == 'VAZIO':
            print(f"   ❌ {key}: VAZIO", flush=True)
            all_ok = False
        else:
            print(f"   ✅ {key}: {val}", flush=True)
    
    if all_ok:
        # Scroll simulation
        print("\n8️⃣  Simulando scroll...", flush=True)
        scroll_amount = random.randint(200, 500)
        driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
        time.sleep(random.uniform(0.5, 1.0))
        driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(0.5)
        
        print("\n9️⃣  Submetendo...", flush=True)
        driver.execute_script("document.querySelector('form').submit();")
        time.sleep(5)
        
        url = driver.current_url
        print(f"\n📄 URL: {url}", flush=True)
        
        if "/do/list/" in url:
            print(f"\n🎉 SUCESSO em {selected_lang['name']}!", flush=True)
            articles = driver.find_elements(By.CSS_SELECTOR, "section.newcarlist article")
            print(f"🚗 {len(articles)} carros encontrados", flush=True)
            
            if len(articles) > 0:
                print("\n📊 Primeiros 5 carros:", flush=True)
                for i, art in enumerate(articles[:5], 1):
                    try:
                        car = art.find_element(By.CSS_SELECTOR, "h2").text
                        price = art.find_element(By.CSS_SELECTOR, ".pr-euros").text
                        print(f"  {i}. {car} - {price}", flush=True)
                    except:
                        print(f"  {i}. [Erro]", flush=True)
        elif "war=" in url:
            war = url.split("war=")[1].split("&")[0]
            print(f"\n❌ ERRO: war={war}", flush=True)
        else:
            print(f"\n⚠️  URL inesperada", flush=True)
    else:
        print("\n❌ Campos vazios!", flush=True)
    
    print("\n⏱️  Chrome aberto 90 segundos", flush=True)
    time.sleep(90)
    
except Exception as e:
    print(f"\n❌ ERRO: {e}", flush=True)
    import traceback
    traceback.print_exc()
    time.sleep(30)
finally:
    driver.quit()
    print("\n👋 Fechado", flush=True)
