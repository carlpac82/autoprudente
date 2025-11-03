#!/usr/bin/env python3
"""
Teste com os NOMES CORRETOS dos campos do Carjet
fechaDevolucion (não fechaEntrega)
fechaDevolucionSelHour (não fechaEntregaSelHour)
"""
import sys
import time
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

print("=" * 80, flush=True)
print("TESTE COM NOMES CORRETOS DOS CAMPOS", flush=True)
print("=" * 80, flush=True)

start_dt = datetime.now() + timedelta(days=7)
end_dt = start_dt + timedelta(days=5)

chrome_options = Options()
chrome_options.add_argument('--start-maximized')

print("\n🚀 Iniciando Chrome...", flush=True)
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

def accept_cookies():
    driver.execute_script("""
        const buttons = document.querySelectorAll('button');
        for (let btn of buttons) {
            if (btn.textContent.toLowerCase().includes('aceitar todos')) {
                btn.click();
                break;
            }
        }
        document.querySelectorAll('[id*=cookie], [class*=cookie]').forEach(el => el.remove());
    """)

try:
    print("\n1️⃣  Abrindo página...", flush=True)
    driver.get("https://www.carjet.com/aluguel-carros/index.htm")
    time.sleep(2)
    accept_cookies()
    time.sleep(1)
    
    print("\n2️⃣  Preenchendo local...", flush=True)
    pickup = driver.find_element(By.ID, "pickup")
    pickup.clear()
    pickup.send_keys("Albufeira Cidade")
    time.sleep(2)
    driver.execute_script("document.querySelector('#recogida_lista li[data-id=\"Albufeira Cidade\"]').click();")
    time.sleep(1)
    accept_cookies()
    
    print("\n3️⃣  Preenchendo datas COM NOMES CORRETOS...", flush=True)
    result = driver.execute_script("""
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
        
        // NOMES CORRETOS DO CARJET
        const r1 = fill('input[name="fechaRecogida"]', arguments[0]) || fill('input[id="fechaRecogida"]', arguments[0]);
        const r2 = fill('input[name="fechaDevolucion"]', arguments[1]) || fill('input[id="fechaDevolucion"]', arguments[1]);
        
        const h1 = document.querySelector('select[name="fechaRecogidaSelHour"]') || document.querySelector('select[id="fechaRecogidaSelHour"]');
        const h2 = document.querySelector('select[name="fechaDevolucionSelHour"]') || document.querySelector('select[id="fechaDevolucionSelHour"]');
        
        let h1_ok = false, h2_ok = false;
        if (h1) { h1.value = '10:00'; h1_ok = true; }
        if (h2) { h2.value = '10:00'; h2_ok = true; }
        
        return {
            fechaRecogida: r1,
            fechaDevolucion: r2,
            horaRecogida: h1_ok,
            horaDevolucion: h2_ok,
            allFilled: r1 && r2 && h1_ok && h2_ok
        };
    """, 
    start_dt.strftime("%d/%m/%Y"),
    end_dt.strftime("%d/%m/%Y")
    )
    
    print(f"   Resultado: {result}", flush=True)
    
    if result.get('allFilled'):
        print(f"   ✅ TUDO PREENCHIDO!", flush=True)
    else:
        print(f"   ⚠️  Incompleto, tentando novamente...", flush=True)
        accept_cookies()
        time.sleep(1)
        # Retry
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
            const h2 = document.querySelector('select[id="fechaDevolucionSelHour"]');
            if (h1) h1.value = '10:00';
            if (h2) h2.value = '10:00';
            return {r1, r2, h1: !!h1, h2: !!h2};
        """, 
        start_dt.strftime("%d/%m/%Y"),
        end_dt.strftime("%d/%m/%Y")
        )
        print(f"   Retry: {result}", flush=True)
    
    time.sleep(1)
    
    # Verificar valores finais
    print("\n🔍 Verificando valores...", flush=True)
    values = driver.execute_script("""
        return {
            pickup: document.querySelector('input[id="pickup"]')?.value || 'N/A',
            fechaRecogida: document.querySelector('input[id="fechaRecogida"]')?.value || 'N/A',
            fechaDevolucion: document.querySelector('input[id="fechaDevolucion"]')?.value || 'N/A',
            horaRecogida: document.querySelector('select[id="fechaRecogidaSelHour"]')?.value || 'N/A',
            horaDevolucion: document.querySelector('select[id="fechaDevolucionSelHour"]')?.value || 'N/A'
        };
    """)
    
    for key, val in values.items():
        status = "✅" if val != 'N/A' else "❌"
        print(f"   {status} {key}: '{val}'", flush=True)
    
    accept_cookies()
    
    print("\n4️⃣  Submetendo formulário...", flush=True)
    driver.execute_script("document.querySelector('form').submit();")
    time.sleep(5)
    accept_cookies()
    time.sleep(2)
    
    url = driver.current_url
    print(f"\n📄 URL final: {url}", flush=True)
    
    if "/do/list/" in url:
        print("\n🎉 SUCESSO! Chegou nos resultados!", flush=True)
        articles = driver.find_elements(By.CSS_SELECTOR, "section.newcarlist article")
        print(f"🚗 {len(articles)} carros encontrados", flush=True)
    elif "war=" in url:
        war = url.split("war=")[1].split("&")[0]
        print(f"\n❌ ERRO: war={war}", flush=True)
    else:
        print(f"\n⚠️  URL inesperada", flush=True)
    
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
