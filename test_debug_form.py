#!/usr/bin/env python3
"""
Teste DEBUG - Mostra exatamente o que foi preenchido
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
print("TESTE DEBUG - VERIFICAR FORMULÁRIO", flush=True)
print("=" * 80, flush=True)

# Datas
start_dt = datetime.now() + timedelta(days=7)
end_dt = start_dt + timedelta(days=5)

print(f"\nDatas esperadas:", flush=True)
print(f"  Recolha: {start_dt.strftime('%d/%m/%Y')} às 10:00", flush=True)
print(f"  Entrega: {end_dt.strftime('%d/%m/%Y')} às 10:00", flush=True)

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
    
    # Clicar dropdown
    driver.execute_script("document.querySelector('#recogida_lista li[data-id=\"Albufeira Cidade\"]').click();")
    time.sleep(1)
    accept_cookies()
    
    print("\n3️⃣  Preenchendo datas e horas...", flush=True)
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
        
        const r1 = fill('input[name="dropoff"]', arguments[0]);
        const r2 = fill('input[name="fechaRecogida"]', arguments[1]);
        const r3 = fill('input[name="fechaEntrega"]', arguments[2]);
        
        const h1 = document.querySelector('select[name="fechaRecogidaSelHour"]');
        const h2 = document.querySelector('select[name="fechaEntregaSelHour"]');
        let h1_ok = false, h2_ok = false;
        if (h1) { h1.value = '10:00'; h1_ok = true; }
        if (h2) { h2.value = '10:00'; h2_ok = true; }
        
        return {
            dropoff: r1,
            fechaRecogida: r2,
            fechaEntrega: r3,
            horaRecogida: h1_ok,
            horaEntrega: h2_ok
        };
    """, 
    "Albufeira Cidade",
    start_dt.strftime("%d/%m/%Y"),
    end_dt.strftime("%d/%m/%Y")
    )
    print(f"   Resultado: {result}", flush=True)
    time.sleep(1)
    
    # VERIFICAR valores preenchidos
    print("\n🔍 Verificando valores no formulário...", flush=True)
    values = driver.execute_script("""
        return {
            pickup: document.querySelector('input[name="pickup"]')?.value || 'N/A',
            dropoff: document.querySelector('input[name="dropoff"]')?.value || 'N/A',
            fechaRecogida: document.querySelector('input[name="fechaRecogida"]')?.value || 'N/A',
            fechaEntrega: document.querySelector('input[name="fechaEntrega"]')?.value || 'N/A',
            horaRecogida: document.querySelector('select[name="fechaRecogidaSelHour"]')?.value || 'N/A',
            horaEntrega: document.querySelector('select[name="fechaEntregaSelHour"]')?.value || 'N/A'
        };
    """)
    
    print(f"\n📋 Valores atuais no formulário:", flush=True)
    for key, val in values.items():
        print(f"   {key}: '{val}'", flush=True)
    
    accept_cookies()
    
    print("\n4️⃣  Submetendo formulário...", flush=True)
    driver.execute_script("document.querySelector('form').submit();")
    
    print("\n⏳ Aguardando 7 segundos...", flush=True)
    time.sleep(7)
    accept_cookies()
    time.sleep(2)
    
    url = driver.current_url
    print(f"\n📄 URL final: {url}", flush=True)
    
    if "war=" in url:
        war_code = url.split("war=")[1].split("&")[0]
        print(f"❌ ERRO: war={war_code}", flush=True)
        print(f"   Possíveis causas:", flush=True)
        print(f"   - war=11: Datas inválidas ou faltando", flush=True)
        print(f"   - war=12: Horas inválidas", flush=True)
        print(f"   - war=13: Local inválido", flush=True)
    elif "/do/list/" in url:
        print("✅ SUCESSO! Chegou nos resultados!", flush=True)
        articles = driver.find_elements(By.CSS_SELECTOR, "section.newcarlist article")
        print(f"🚗 {len(articles)} carros encontrados", flush=True)
    else:
        print(f"⚠️  URL inesperada", flush=True)
    
    print("\n⏱️  Chrome fica aberto 90 segundos para você inspecionar", flush=True)
    time.sleep(90)
    
except Exception as e:
    print(f"\n❌ ERRO: {e}", flush=True)
    import traceback
    traceback.print_exc()
    time.sleep(30)
finally:
    driver.quit()
    print("\n👋 Chrome fechado", flush=True)
