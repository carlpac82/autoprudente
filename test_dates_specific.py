#!/usr/bin/env python3
"""
Teste específico: 12 a 20 novembro às 15:00
"""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import datetime

print("═" * 80)
print("🧪 TESTE ESPECÍFICO - 12 a 20 NOVEMBRO ÀS 15:00")
print("═" * 80)

# Datas específicas
start_date = datetime(2025, 11, 12, 15, 0)  # 12/11/2025 15:00
end_date = datetime(2025, 11, 20, 15, 0)    # 20/11/2025 15:00
days = (end_date - start_date).days

print(f"📅 Data recolha: {start_date.strftime('%d/%m/%Y')} às {start_date.strftime('%H:%M')}")
print(f"📅 Data devolução: {end_date.strftime('%d/%m/%Y')} às {end_date.strftime('%H:%M')}")
print(f"📊 Total: {days} dias")
print("═" * 80)

# Configurar Chrome
chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1')

# Mobile emulation
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

# Esconder webdriver
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
    
    # Escrever local
    print(f"\n✅ PASSO 1: Escrevendo local...")
    pickup_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "pickup"))
    )
    pickup_input.clear()
    pickup_input.send_keys("Faro Aeroporto (FAO)")
    print(f"   ✓ Local digitado")
    
    # Dropdown
    print(f"\n✅ PASSO 2: Aguardando dropdown...")
    time.sleep(3)
    
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
    
    time.sleep(1)
    
    # Preencher datas e horas
    print(f"\n✅ PASSO 3: Preenchendo datas e horas...")
    print(f"   📅 Recolha: {start_date.strftime('%d/%m/%Y')} às {start_date.strftime('%H:%M')}")
    print(f"   📅 Devolução: {end_date.strftime('%d/%m/%Y')} às {end_date.strftime('%H:%M')}")
    
    result = driver.execute_script("""
        function fill(sel, val) {
            const el = document.querySelector(sel);
            if (el) { 
                el.value = val; 
                el.dispatchEvent(new Event('input', {bubbles: true}));
                el.dispatchEvent(new Event('change', {bubbles: true}));
                el.dispatchEvent(new Event('blur', {bubbles: true}));
                console.log('Preenchido:', sel, '=', val);
                return true;
            }
            console.error('Não encontrado:', sel);
            return false;
        }
        
        // Preencher datas
        const r1 = fill('input[id="fechaRecogida"]', arguments[0]);
        const r2 = fill('input[id="fechaDevolucion"]', arguments[1]);
        
        // Preencher horas
        const h1 = document.querySelector('select[id="fechaRecogidaSelHour"]');
        let h1_ok = false;
        if (h1) { 
            h1.value = arguments[2]; 
            h1.dispatchEvent(new Event('change', {bubbles: true}));
            console.log('Hora recolha:', h1.value);
            h1_ok = true;
        }
        
        const h2 = document.querySelector('select[id="fechaDevolucionSelHour"]');
        let h2_ok = false;
        if (h2) { 
            h2.value = arguments[3]; 
            h2.dispatchEvent(new Event('change', {bubbles: true}));
            console.log('Hora devolução:', h2.value);
            h2_ok = true;
        }
        
        return {
            fechaRecogida: r1,
            fechaDevolucion: r2,
            horaRecogida: h1_ok,
            horaDevolucion: h2_ok,
            horaRecogidaValue: h1 ? h1.value : null,
            horaDevolucionValue: h2 ? h2.value : null,
            allFilled: r1 && r2 && h1_ok && h2_ok
        };
    """, start_date.strftime("%d/%m/%Y"), end_date.strftime("%d/%m/%Y"), "15:00", "15:00")
    
    print(f"\n📊 RESULTADO DO PREENCHIMENTO:")
    print(f"   Data recolha: {'✅' if result.get('fechaRecogida') else '❌'}")
    print(f"   Data devolução: {'✅' if result.get('fechaDevolucion') else '❌'}")
    print(f"   Hora recolha: {'✅' if result.get('horaRecogida') else '❌'} (valor: {result.get('horaRecogidaValue')})")
    print(f"   Hora devolução: {'✅' if result.get('horaDevolucion') else '❌'} (valor: {result.get('horaDevolucionValue')})")
    print(f"   Tudo preenchido: {'✅' if result.get('allFilled') else '❌'}")
    
    # Verificar valores atuais no formulário
    print(f"\n🔍 VERIFICANDO VALORES NO FORMULÁRIO:")
    verification = driver.execute_script("""
        return {
            fechaRecogida: document.querySelector('input[id="fechaRecogida"]')?.value,
            fechaDevolucion: document.querySelector('input[id="fechaDevolucion"]')?.value,
            horaRecogida: document.querySelector('select[id="fechaRecogidaSelHour"]')?.value,
            horaDevolucion: document.querySelector('select[id="fechaDevolucionSelHour"]')?.value
        };
    """)
    print(f"   📅 Data recolha no form: {verification.get('fechaRecogida')}")
    print(f"   📅 Data devolução no form: {verification.get('fechaDevolucion')}")
    print(f"   ⏰ Hora recolha no form: {verification.get('horaRecogida')}")
    print(f"   ⏰ Hora devolução no form: {verification.get('horaDevolucion')}")
    
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
    
    print(f"\n⏳ Mantendo Chrome aberto por 30 segundos para você ver...")
    time.sleep(30)
    
except Exception as e:
    print(f"\n❌ ERRO: {e}")
    import traceback
    traceback.print_exc()
    time.sleep(30)
finally:
    driver.quit()
    print("\n✅ Chrome fechado")
    print("═" * 80)
