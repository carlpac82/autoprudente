#!/usr/bin/env python3
"""
Teste FINAL: REJEITAR cookies em vez de aceitar
"""
import sys
import time
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

print("=" * 80, flush=True)
print("TESTE - REJEITAR COOKIES", flush=True)
print("=" * 80, flush=True)

start_dt = datetime.now() + timedelta(days=7)
end_dt = start_dt + timedelta(days=5)

mobile_ua = "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1"

chrome_options = Options()
chrome_options.add_argument('--start-maximized')
chrome_options.add_argument(f'user-agent={mobile_ua}')

mobile_emulation = {
    "deviceMetrics": { "width": 375, "height": 812, "pixelRatio": 3.0 },
    "userAgent": mobile_ua
}
chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)

print("\n🚀 Iniciando Chrome MOBILE...", flush=True)
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

def reject_cookies():
    """REJEITA cookies"""
    try:
        result = driver.execute_script("""
            const buttons = document.querySelectorAll('button, a, [role="button"]');
            for (let btn of buttons) {
                const text = btn.textContent.toLowerCase().trim();
                if (text.includes('rejeitar') || text.includes('recusar') || 
                    text.includes('reject') || text.includes('decline')) {
                    btn.click();
                    return {success: true, text: btn.textContent.trim()};
                }
            }
            // Se não encontrou, remover banner
            document.querySelectorAll('[id*=cookie], [class*=cookie]').forEach(el => el.remove());
            return {success: false, text: 'Banner removido'};
        """)
        if result['success']:
            print(f"   ✅ Cookies rejeitados: '{result['text']}'", flush=True)
        else:
            print(f"   ℹ️  {result['text']}", flush=True)
        return result['success']
    except Exception as e:
        print(f"   ❌ Erro: {e}", flush=True)
        return False

try:
    print("\n1️⃣  Abrindo página...", flush=True)
    driver.get("https://www.carjet.com/aluguel-carros/index.htm")
    
    print("\n🍪 Rejeitando cookies...", flush=True)
    time.sleep(0.5)
    reject_cookies()
    time.sleep(0.5)
    reject_cookies()  # Retry
    time.sleep(0.5)
    
    print("\n2️⃣  Preenchendo local...", flush=True)
    pickup = driver.find_element(By.ID, "pickup")
    pickup.clear()
    pickup.send_keys("Albufeira Cidade")
    time.sleep(2)
    driver.execute_script("document.querySelector('#recogida_lista li[data-id=\"Albufeira Cidade\"]').click();")
    print("   ✅ Local preenchido", flush=True)
    time.sleep(1)
    reject_cookies()
    
    print("\n3️⃣  Preenchendo formulário...", flush=True)
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
        
        const pickup = fill('input[id="pickup"]', arguments[0]);
        const r1 = fill('input[id="fechaRecogida"]', arguments[1]);
        const r2 = fill('input[id="fechaDevolucion"]', arguments[2]);
        const h1 = document.querySelector('select[id="fechaRecogidaSelHour"]');
        const h2 = document.querySelector('select[id="fechaDevolucionSelHour"]');
        if (h1) h1.value = '10:00';
        if (h2) h2.value = '10:00';
        
        return {pickup, r1, r2, h1: !!h1, h2: !!h2, allFilled: pickup && r1 && r2 && h1 && h2};
    """, 
    "Albufeira Cidade",
    start_dt.strftime("%d/%m/%Y"),
    end_dt.strftime("%d/%m/%Y")
    )
    
    print(f"   Resultado: {result}", flush=True)
    
    print("\n4️⃣  Verificando valores...", flush=True)
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
        reject_cookies()
        
        print("\n5️⃣  Submetendo...", flush=True)
        driver.execute_script("document.querySelector('form').submit();")
        time.sleep(5)
        reject_cookies()
        time.sleep(2)
        
        url = driver.current_url
        print(f"\n📄 URL: {url}", flush=True)
        
        if "/do/list/" in url:
            print("\n🎉 SUCESSO TOTAL!", flush=True)
            articles = driver.find_elements(By.CSS_SELECTOR, "section.newcarlist article")
            print(f"🚗 {len(articles)} carros encontrados", flush=True)
        elif "war=" in url:
            war = url.split("war=")[1].split("&")[0]
            print(f"\n❌ ERRO: war={war}", flush=True)
        else:
            print(f"\n⚠️  URL inesperada", flush=True)
    else:
        print("\n❌ Campos vazios!", flush=True)
    
    print("\n⏱️  Chrome aberto 60 segundos", flush=True)
    time.sleep(60)
    
except Exception as e:
    print(f"\n❌ ERRO: {e}", flush=True)
    import traceback
    traceback.print_exc()
    time.sleep(30)
finally:
    driver.quit()
    print("\n👋 Fechado", flush=True)
