#!/usr/bin/env python3
"""
Teste para mostrar qual dispositivo está sendo usado
"""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import datetime, timedelta
import random

print("═" * 80)
print("🔍 TESTE DE DISPOSITIVO - CARJET SCRAPING")
print("═" * 80)

# DISPOSITIVOS DISPONÍVEIS (igual ao main.py)
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

# SELECIONAR ALEATORIAMENTE
selected_device = random.choice(mobile_devices)

print(f"\n📱 DISPOSITIVO SELECIONADO:")
print(f"   Nome: {selected_device['name']}")
print(f"   Resolução: {selected_device['width']}x{selected_device['height']}")
print(f"   Pixel Ratio: {selected_device['pixelRatio']}")
print(f"   User Agent: {selected_device['ua'][:80]}...")

# IDIOMAS
languages = [
    {'name': 'Português', 'url': 'https://www.carjet.com/aluguel-carros/index.htm', 'faro': 'Faro Aeroporto (FAO)'},
    {'name': 'English', 'url': 'https://www.carjet.com/index.htm', 'faro': 'Faro Airport (FAO)'},
]
selected_language = random.choice(languages)

print(f"\n🌍 IDIOMA SELECIONADO:")
print(f"   {selected_language['name']}")
print(f"   URL: {selected_language['url']}")

# TIMEZONES
timezones = ['Europe/Lisbon', 'Europe/Madrid', 'Europe/London', 'Europe/Paris']
selected_timezone = random.choice(timezones)

print(f"\n🕐 TIMEZONE SELECIONADO:")
print(f"   {selected_timezone}")

# REFERRERS
referrers = [
    'https://www.google.com/search?q=aluguer+carros+faro',
    'https://www.google.pt/search?q=rent+car+portugal',
    'https://www.bing.com/search?q=car+rental+algarve',
    'https://www.booking.com/',
    ''  # Direct
]
selected_referrer = random.choice(referrers)

print(f"\n🔗 REFERRER SELECIONADO:")
print(f"   {selected_referrer if selected_referrer else 'Direct (sem referrer)'}")

# HORAS
available_hours = ['14:30', '15:00', '15:30', '16:00', '16:30', '17:00']
selected_hour = random.choice(available_hours)

print(f"\n⏰ HORA SELECIONADA:")
print(f"   {selected_hour}")

print("\n" + "═" * 80)
print("🚀 Iniciando Chrome com estas configurações...")
print("═" * 80)

# Configurar Chrome
chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument(f'user-agent={selected_device["ua"]}')

# Emulação mobile
mobile_emulation = {
    "deviceMetrics": { 
        "width": selected_device['width'], 
        "height": selected_device['height'], 
        "pixelRatio": selected_device['pixelRatio']
    },
    "userAgent": selected_device['ua']
}
chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)

# Anti-detecção
chrome_options.add_argument('--disable-blink-features=AutomationControlled')
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)

# Timezone
chrome_options.add_argument(f'--timezone={selected_timezone}')

# Caminho do Chrome
chrome_options.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

driver = webdriver.Chrome(options=chrome_options)

# Esconder webdriver
driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
    'source': '''
        Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined
        });
    '''
})

# Definir referrer
if selected_referrer:
    driver.execute_cdp_cmd('Network.setExtraHTTPHeaders', {
        'headers': {'Referer': selected_referrer}
    })

driver.set_page_load_timeout(20)

# Função para rejeitar cookies
def reject_cookies():
    try:
        result = driver.execute_script("""
            const buttons = document.querySelectorAll('button, a, [role="button"]');
            let found = false;
            for (let btn of buttons) {
                const text = btn.textContent.toLowerCase().trim();
                if (text.includes('rejeitar') || text.includes('recusar') || 
                    text.includes('reject') || text.includes('decline')) {
                    btn.click();
                    found = true;
                    break;
                }
            }
            if (!found) {
                document.querySelectorAll('[id*=cookie], [class*=cookie], [id*=didomi]').forEach(el => {
                    el.remove();
                });
            }
            return found;
        """)
        return result
    except:
        return False

try:
    # Navegar
    print(f"\n📱 Navegando para {selected_language['url']}")
    driver.get(selected_language['url'])
    
    # Cookies
    print(f"\n✅ PASSO 1: Rejeitando cookies...")
    time.sleep(0.5)
    if reject_cookies():
        print(f"   ✓ Cookies rejeitados")
    time.sleep(0.5)
    
    # Escrever local
    print(f"\n✅ PASSO 2: Escrevendo local...")
    carjet_location = selected_language['faro']
    pickup_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "pickup"))
    )
    pickup_input.clear()
    pickup_input.send_keys(carjet_location)
    print(f"   ✓ Local digitado: {carjet_location}")
    
    # Dropdown
    print(f"\n✅ PASSO 3: Aguardando dropdown (3 segundos)...")
    time.sleep(3)
    
    # Ver quantos items
    dropdown_info = driver.execute_script("""
        const lista = document.querySelector('#recogida_lista');
        if (!lista) return 'Dropdown não encontrado';
        const items = lista.querySelectorAll('li');
        return items.length;
    """)
    print(f"   🔍 Dropdown tem {dropdown_info} items")
    
    # Clicar
    clicked = False
    try:
        dropdown_item = WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#recogida_lista li:first-child a"))
        )
        dropdown_item.click()
        clicked = True
        print(f"   ✅ Dropdown clicado!")
    except:
        print(f"   ⚠️ Falhou com CSS, tentando JavaScript...")
        result = driver.execute_script("""
            const items = document.querySelectorAll('#recogida_lista li');
            for (let item of items) {
                if (item.offsetParent !== null) {
                    item.click();
                    return true;
                }
            }
            return false;
        """)
        if result:
            clicked = True
            print(f"   ✅ Dropdown clicado via JavaScript!")
    
    if not clicked:
        print(f"   ❌ NÃO CONSEGUIU CLICAR!")
    
    time.sleep(1)
    
    # Datas e horas
    print(f"\n✅ PASSOS 4-7: Preenchendo datas e horas...")
    start_date = datetime.now() + timedelta(days=7)
    end_date = start_date + timedelta(days=3)
    
    result = driver.execute_script("""
        function fill(sel, val) {
            const el = document.querySelector(sel);
            if (el) { 
                el.value = val; 
                el.dispatchEvent(new Event('change', {bubbles: true}));
                return true;
            }
            return false;
        }
        
        const r1 = fill('input[id="fechaRecogida"]', arguments[0]);
        const r2 = fill('input[id="fechaDevolucion"]', arguments[1]);
        
        const h1 = document.querySelector('select[id="fechaRecogidaSelHour"]');
        let h1_ok = false;
        if (h1) { 
            h1.value = arguments[2]; 
            h1.dispatchEvent(new Event('change'));
            h1_ok = true;
        }
        
        const h2 = document.querySelector('select[id="fechaDevolucionSelHour"]');
        let h2_ok = false;
        if (h2) { 
            h2.value = arguments[3]; 
            h2.dispatchEvent(new Event('change'));
            h2_ok = true;
        }
        
        return {r1, r2, h1_ok, h2_ok, all: r1 && r2 && h1_ok && h2_ok};
    """, start_date.strftime("%d/%m/%Y"), end_date.strftime("%d/%m/%Y"), selected_hour, selected_hour)
    
    if result.get('all'):
        print(f"   ✅ Formulário completo!")
    
    # Submit
    print(f"\n✅ PASSO 8: Submetendo...")
    driver.execute_script("window.scrollBy(0, 300);")
    time.sleep(0.5)
    driver.execute_script("window.scrollTo(0, 0);")
    time.sleep(0.5)
    driver.execute_script("document.querySelector('form').submit();")
    
    print(f"\n⏳ Aguardando navegação...")
    time.sleep(5)
    
    final_url = driver.current_url
    print(f"\n📍 URL FINAL:")
    print(f"   {final_url}")
    
    if '/do/list/' in final_url and 's=' in final_url and 'b=' in final_url:
        print(f"\n✅ ✅ ✅ SUCESSO! ✅ ✅ ✅")
    elif 'war=' in final_url:
        print(f"\n⚠️ URL com war=")
    
    print(f"\n" + "═" * 80)
    print(f"📊 RESUMO DAS ROTAÇÕES USADAS:")
    print(f"   📱 Device: {selected_device['name']}")
    print(f"   🌍 Idioma: {selected_language['name']}")
    print(f"   🕐 Timezone: {selected_timezone}")
    print(f"   🔗 Referrer: {selected_referrer if selected_referrer else 'Direct'}")
    print(f"   ⏰ Hora: {selected_hour}")
    print(f"═" * 80)
    
    print(f"\n⏳ Mantendo Chrome aberto por 20 segundos...")
    time.sleep(20)
    
except Exception as e:
    print(f"\n❌ ERRO: {e}")
    import traceback
    traceback.print_exc()
    time.sleep(30)
finally:
    driver.quit()
    print("\n✅ Chrome fechado")
