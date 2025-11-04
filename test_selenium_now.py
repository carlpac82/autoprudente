#!/usr/bin/env python3
"""
Teste do Selenium com os 8 passos do Carjet
Mostra o Chrome visível para debug
"""
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import datetime, timedelta
import random

# Dados do teste
location = "Faro"
start_date = datetime.now() + timedelta(days=7)
end_date = start_date + timedelta(days=3)

print("═" * 80)
print("🧪 TESTE DO SELENIUM - CARJET SCRAPING")
print("═" * 80)
print(f"📍 Local: {location}")
print(f"📅 Recolha: {start_date.strftime('%d/%m/%Y')} às 15:00")
print(f"📅 Devolução: {end_date.strftime('%d/%m/%Y')} às 15:00")
print("═" * 80)

# Idioma aleatório
languages = [
    {'name': 'Português', 'url': 'https://www.carjet.com/aluguel-carros/index.htm', 'faro': 'Faro Aeroporto (FAO)'},
    {'name': 'English', 'url': 'https://www.carjet.com/index.htm', 'faro': 'Faro Airport (FAO)'},
]
selected_language = random.choice(languages)
carjet_location = selected_language['faro']
carjet_url = selected_language['url']

print(f"\n🌍 Idioma: {selected_language['name']}")
print(f"🔗 URL: {carjet_url}")
print(f"📍 Local traduzido: {carjet_location}")

# Dispositivo mobile
selected_device = {
    'name': 'iPhone 13',
    'ua': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1',
    'width': 390, 'height': 844, 'pixelRatio': 3.0
}

print(f"📱 Device: {selected_device['name']}")
print("\n" + "═" * 80)

# Configurar Chrome
chrome_options = Options()
# NÃO usar headless para ver o que está acontecendo
# chrome_options.add_argument('--headless')
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

# Caminho do Chrome no Mac
chrome_options.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

print("🚀 Iniciando Chrome...")
driver = webdriver.Chrome(options=chrome_options)

# Esconder webdriver
driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
    'source': '''
        Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined
        });
    '''
})

driver.set_page_load_timeout(20)

# Função para rejeitar cookies
def reject_cookies_if_present(step_name=""):
    try:
        result = driver.execute_script("""
            const buttons = document.querySelectorAll('button, a, [role="button"]');
            let found = false;
            for (let btn of buttons) {
                const text = btn.textContent.toLowerCase().trim();
                if (text.includes('rejeitar') || text.includes('recusar') || 
                    text.includes('reject') || text.includes('rechazar') ||
                    text.includes('não aceitar') || text.includes('decline')) {
                    btn.click();
                    found = true;
                    break;
                }
            }
            if (!found) {
                document.querySelectorAll('[id*=cookie], [class*=cookie], [id*=didomi], [class*=didomi]').forEach(el => {
                    el.remove();
                });
            }
            document.body.style.overflow = 'auto';
            return found;
        """)
        if result:
            print(f"   ✓ Cookies rejeitados {step_name}")
        return result
    except Exception as e:
        print(f"   ⚠ Erro ao rejeitar cookies: {e}")
        return False

try:
    # Navegar
    print(f"\n📱 Navegando para {carjet_url}")
    driver.get(carjet_url)
    
    # PASSO 1: COOKIES
    print(f"\n✅ PASSO 1: Rejeitando cookies...")
    time.sleep(0.5)
    reject_cookies_if_present("(inicial)")
    time.sleep(0.5)
    reject_cookies_if_present("(retry)")
    time.sleep(0.5)
    
    # PASSO 2: ESCREVER LOCAL
    print(f"\n✅ PASSO 2: Escrevendo local '{carjet_location}'...")
    pickup_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "pickup"))
    )
    pickup_input.clear()
    pickup_input.send_keys(carjet_location)
    print(f"   ✓ Local digitado")
    
    # PASSO 3: CLICAR NO DROPDOWN ⚠️ CRÍTICO!
    print(f"\n✅ PASSO 3: Aguardando dropdown aparecer...")
    time.sleep(3)
    
    # DEBUG: Ver dropdown
    dropdown_info = driver.execute_script("""
        const lista = document.querySelector('#recogida_lista');
        if (!lista) return 'Dropdown não encontrado';
        const items = lista.querySelectorAll('li');
        return `Dropdown com ${items.length} items`;
    """)
    print(f"   🔍 DEBUG: {dropdown_info}")
    
    clicked = False
    selectors = [
        "#recogida_lista li:first-child a",
        "#recogida_lista li:first-child",
    ]
    
    for selector in selectors:
        if clicked:
            break
        try:
            print(f"   Tentando: {selector}")
            dropdown_item = WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
            )
            dropdown_item.click()
            clicked = True
            print(f"   ✅ Dropdown clicado via: {selector}")
            break
        except Exception as e:
            print(f"   ⚠ Falhou: {str(e)[:50]}")
    
    # Fallback JavaScript
    if not clicked:
        print(f"   Tentando via JavaScript...")
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
            print(f"   ✅ Dropdown clicado via JavaScript")
    
    if not clicked:
        print(f"   ❌ NÃO CONSEGUIU CLICAR NO DROPDOWN!")
        print(f"\n⏳ Mantendo Chrome aberto por 60 segundos para você ver...")
        time.sleep(60)
        driver.quit()
        exit(1)
    
    time.sleep(1)
    
    # PASSOS 4-7: PREENCHER DATAS E HORAS
    print(f"\n✅ PASSOS 4-7: Preenchendo datas e horas...")
    result = driver.execute_script("""
        function fill(sel, val) {
            const el = document.querySelector(sel);
            if (el) { 
                el.value = val; 
                el.dispatchEvent(new Event('input', {bubbles: true}));
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
            h1.dispatchEvent(new Event('change', {bubbles: true}));
            h1_ok = true;
        }
        
        const h2 = document.querySelector('select[id="fechaDevolucionSelHour"]');
        let h2_ok = false;
        if (h2) { 
            h2.value = arguments[3]; 
            h2.dispatchEvent(new Event('change', {bubbles: true}));
            h2_ok = true;
        }
        
        return {
            fechaRecogida: r1,
            fechaDevolucion: r2,
            horaRecogida: h1_ok,
            horaDevolucion: h2_ok,
            allFilled: r1 && r2 && h1_ok && h2_ok
        };
    """, start_date.strftime("%d/%m/%Y"), end_date.strftime("%d/%m/%Y"), "15:00", "15:00")
    
    print(f"   ✓ Data recolha: {result.get('fechaRecogida', False)}")
    print(f"   ✓ Data devolução: {result.get('fechaDevolucion', False)}")
    print(f"   ✓ Hora recolha: {result.get('horaRecogida', False)}")
    print(f"   ✓ Hora devolução: {result.get('horaDevolucion', False)}")
    
    if result.get('allFilled'):
        print(f"   ✅ Formulário completo!")
    
    time.sleep(1)
    
    # PASSO 8: SUBMETER
    print(f"\n✅ PASSO 8: Submetendo formulário...")
    
    # Scroll
    driver.execute_script("window.scrollBy(0, 300);")
    time.sleep(0.5)
    driver.execute_script("window.scrollTo(0, 0);")
    time.sleep(0.5)
    
    # Submit
    driver.execute_script("document.querySelector('form').submit();")
    print(f"   ✓ Formulário submetido")
    
    # Aguardar
    print(f"\n⏳ Aguardando navegação...")
    time.sleep(5)
    
    final_url = driver.current_url
    print(f"\n📍 URL FINAL:")
    print(f"   {final_url}")
    
    if '/do/list/' in final_url and 's=' in final_url and 'b=' in final_url:
        print(f"\n✅ ✅ ✅ SUCESSO TOTAL! ✅ ✅ ✅")
        print(f"URL válida com s= e b=")
    elif 'war=' in final_url:
        print(f"\n⚠️ URL contém war= (sem disponibilidade ou erro)")
    else:
        print(f"\n⚠️ URL inesperada")
    
    print(f"\n⏳ Mantendo Chrome aberto por 30 segundos para você ver...")
    time.sleep(30)
    
except KeyboardInterrupt:
    print("\n\n🛑 Interrompido")
except Exception as e:
    print(f"\n❌ ERRO: {e}")
    import traceback
    traceback.print_exc()
    print(f"\n⏳ Mantendo Chrome aberto por 60 segundos para debug...")
    time.sleep(60)
finally:
    driver.quit()
    print("\n✅ Chrome fechado")
    print("═" * 80)
