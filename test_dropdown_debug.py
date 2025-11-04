#!/usr/bin/env python3
"""
Debug version - Monitor dropdown behavior in detail
"""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import datetime

print("=" * 80)
print("🔍 DROPDOWN DEBUG - Monitoring ALL events")
print("=" * 80)

# Datas
start_date = datetime(2025, 11, 12, 15, 0)
end_date = datetime(2025, 11, 20, 15, 0)

# Chrome config (IGUAL AO TESTE)
chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1')

mobile_emulation = {
    "deviceMetrics": {"width": 390, "height": 844, "pixelRatio": 3.0},
    "userAgent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1"
}
chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
chrome_options.add_argument('--disable-blink-features=AutomationControlled')
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)
chrome_options.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

driver = webdriver.Chrome(options=chrome_options)

driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
    'source': 'Object.defineProperty(navigator, "webdriver", { get: () => undefined });'
})

driver.set_page_load_timeout(20)

def reject_cookies():
    try:
        result = driver.execute_script("""
            const buttons = document.querySelectorAll('button, a, [role="button"]');
            for (let btn of buttons) {
                const text = btn.textContent.toLowerCase().trim();
                if (text.includes('rejeitar') || text.includes('reject')) {
                    btn.click();
                    return true;
                }
            }
            return false;
        """)
        return result
    except:
        return False

try:
    # Navegar
    url = "https://www.carjet.com/aluguel-carros/index.htm"
    print(f"\n🌐 Navegando para {url}")
    driver.get(url)
    
    # Cookies
    time.sleep(0.5)
    if reject_cookies():
        print("   ✅ Cookies rejeitados")
    time.sleep(0.5)
    
    # INSTALAR MONITORES DE EVENTOS
    print(f"\n🔍 Instalando monitores de eventos...")
    driver.execute_script("""
        window.eventLog = [];
        
        // Monitor pickup field
        const pickup = document.getElementById('pickup');
        if (pickup) {
            ['focus', 'blur', 'click', 'mousedown', 'mouseup', 'keydown', 'keyup', 'change', 'input'].forEach(eventType => {
                pickup.addEventListener(eventType, function(e) {
                    const timestamp = new Date().toISOString().split('T')[1];
                    const log = `[${timestamp}] PICKUP.${eventType}`;
                    console.log(log);
                    window.eventLog.push(log);
                }, true);
            });
            console.log('[MONITOR] Pickup field monitored');
        }
        
        // Monitor dropdown
        const dropdown = document.getElementById('recogida_lista');
        if (dropdown) {
            const observer = new MutationObserver(function(mutations) {
                mutations.forEach(function(mutation) {
                    if (mutation.type === 'attributes' && mutation.attributeName === 'style') {
                        const timestamp = new Date().toISOString().split('T')[1];
                        const isVisible = dropdown.offsetParent !== null;
                        const log = `[${timestamp}] DROPDOWN.visibility=${isVisible}`;
                        console.log(log);
                        window.eventLog.push(log);
                    }
                });
            });
            observer.observe(dropdown, { attributes: true });
            console.log('[MONITOR] Dropdown monitored');
        }
        
        // Monitor date fields
        ['fechaRecogida', 'fechaDevolucion'].forEach(id => {
            const el = document.getElementById(id);
            if (el) {
                ['focus', 'blur', 'change', 'input'].forEach(eventType => {
                    el.addEventListener(eventType, function(e) {
                        const timestamp = new Date().toISOString().split('T')[1];
                        const log = `[${timestamp}] ${id}.${eventType}`;
                        console.log(log);
                        window.eventLog.push(log);
                    }, true);
                });
            }
        });
        
        console.log('[MONITOR] All monitors installed!');
    """)
    print("   ✅ Monitores instalados")
    
    # Escrever local
    print(f"\n✅ PASSO 1: Escrevendo local...")
    pickup_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "pickup"))
    )
    pickup_input.clear()
    pickup_input.send_keys("Faro Aeroporto (FAO)")
    print(f"   ✓ Local digitado")
    
    # Ver eventos até agora
    events = driver.execute_script("return window.eventLog;")
    print(f"\n📊 Eventos após send_keys:")
    for event in events[-10:]:  # Últimos 10
        print(f"   {event}")
    
    # Dropdown
    print(f"\n✅ PASSO 2: Aguardando dropdown...")
    time.sleep(3)
    
    # Ver eventos
    events = driver.execute_script("return window.eventLog;")
    print(f"\n📊 Eventos após aguardar 3s:")
    for event in events[-10:]:
        print(f"   {event}")
    
    try:
        dropdown_item = WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#recogida_lista li:first-child a"))
        )
        dropdown_item.click()
        print(f"   ✅ Dropdown clicado")
    except:
        driver.execute_script("""
            const items = document.querySelectorAll('#recogida_lista li');
            for (let item of items) {
                if (item.offsetParent !== null) {
                    item.click();
                    return true;
                }
            }
        """)
        print(f"   ✅ Dropdown clicado (JS)")
    
    # Ver eventos após clicar
    events = driver.execute_script("return window.eventLog;")
    print(f"\n📊 Eventos após clicar dropdown:")
    for event in events[-10:]:
        print(f"   {event}")
    
    time.sleep(1)
    
    # Preencher datas
    print(f"\n✅ PASSO 3: Preenchendo datas...")
    driver.execute_script("""
        function fill(sel, val) {
            const el = document.querySelector(sel);
            if (el) { 
                el.value = val; 
                el.dispatchEvent(new Event('input', {bubbles: true}));
                el.dispatchEvent(new Event('change', {bubbles: true}));
                el.dispatchEvent(new Event('blur', {bubbles: true}));
                return true;
            }
            return false;
        }
        
        fill('input[id="fechaRecogida"]', arguments[0]);
        fill('input[id="fechaDevolucion"]', arguments[1]);
        
        const h1 = document.querySelector('select[id="fechaRecogidaSelHour"]');
        if (h1) { 
            h1.value = arguments[2]; 
            h1.dispatchEvent(new Event('change', {bubbles: true}));
        }
        
        const h2 = document.querySelector('select[id="fechaDevolucionSelHour"]');
        if (h2) { 
            h2.value = arguments[3]; 
            h2.dispatchEvent(new Event('change', {bubbles: true}));
        }
    """, start_date.strftime("%d/%m/%Y"), end_date.strftime("%d/%m/%Y"), "15:00", "15:00")
    print(f"   ✓ Datas preenchidas")
    
    # Ver eventos após preencher
    events = driver.execute_script("return window.eventLog;")
    print(f"\n📊 Eventos após preencher datas:")
    for event in events[-20:]:
        print(f"   {event}")
    
    # Verificar se dropdown reabriu
    dropdown_visible = driver.execute_script("""
        const dropdown = document.getElementById('recogida_lista');
        return dropdown && dropdown.offsetParent !== null;
    """)
    
    if dropdown_visible:
        print(f"\n⚠️⚠️⚠️ DROPDOWN REABRIU! ⚠️⚠️⚠️")
    else:
        print(f"\n✅ Dropdown continua fechado")
    
    time.sleep(1)
    
    # Submit
    print(f"\n✅ PASSO 4: Submetendo...")
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
        print(f"\n⚠️ URL com war= (sem disponibilidade ou erro)")
    
    # Mostrar TODOS os eventos
    events = driver.execute_script("return window.eventLog;")
    print(f"\n📊 TODOS OS EVENTOS ({len(events)} total):")
    for event in events:
        print(f"   {event}")
    
    print(f"\n⏳ Mantendo Chrome aberto por 30 segundos...")
    time.sleep(30)
    
except Exception as e:
    print(f"\n❌ ERRO: {e}")
    import traceback
    traceback.print_exc()
    time.sleep(30)
finally:
    driver.quit()
    print("\n✅ Chrome fechado")
    print("=" * 80)
