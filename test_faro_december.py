#!/usr/bin/env python3
"""
Teste: Faro Aeroporto, 11-18 Dezembro, 15:30
"""
import sys
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

print("=" * 80, flush=True)
print("TESTE - FARO AEROPORTO 11-18 DEZ 15:30", flush=True)
print("=" * 80, flush=True)

# Datas específicas
start_date = "11/12/2025"
end_date = "18/12/2025"
hora = "15:30"

print(f"\n📋 Parâmetros:", flush=True)
print(f"   Local: Faro Aeroporto (FAO)", flush=True)
print(f"   Recolha: {start_date} às {hora}", flush=True)
print(f"   Devolução: {end_date} às {hora}", flush=True)

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

try:
    print("\n1️⃣  Abrindo página...", flush=True)
    driver.get("https://www.carjet.com/aluguel-carros/index.htm")
    time.sleep(2)
    
    print("\n2️⃣  Removendo cookies...", flush=True)
    driver.execute_script("document.querySelectorAll('[id*=cookie], [class*=cookie]').forEach(el => el.remove());")
    time.sleep(1)
    
    print("\n3️⃣  Preenchendo local: Faro Aeroporto...", flush=True)
    pickup = driver.find_element(By.ID, "pickup")
    pickup.clear()
    pickup.send_keys("Faro Aeroporto")
    print("   ✅ Digitado", flush=True)
    time.sleep(2)
    
    print("\n4️⃣  Clicando no dropdown...", flush=True)
    try:
        # Tentar clicar no item "Faro Aeroporto (FAO)"
        dropdown_item = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#recogida_lista li[data-id='Faro Aeroporto (FAO)']"))
        )
        dropdown_item.click()
        print("   ✅ 'Faro Aeroporto (FAO)' selecionado", flush=True)
    except:
        try:
            # Alternativa: qualquer item com "Faro"
            driver.execute_script("""
                const items = document.querySelectorAll('#recogida_lista li');
                for (let item of items) {
                    if (item.textContent.includes('Faro') && item.textContent.includes('Aeroporto')) {
                        item.click();
                        break;
                    }
                }
            """)
            print("   ✅ Faro selecionado (alternativa)", flush=True)
        except:
            print("   ⚠️  Dropdown não encontrado", flush=True)
    
    time.sleep(2)
    
    print("\n5️⃣  Preenchendo datas...", flush=True)
    # Data de recolha
    driver.execute_script("""
        const fechaRec = document.querySelector('input[id="fechaRecogida"]');
        if (fechaRec) {
            fechaRec.value = arguments[0];
            fechaRec.dispatchEvent(new Event('input', {bubbles: true}));
            fechaRec.dispatchEvent(new Event('change', {bubbles: true}));
        }
    """, start_date)
    print(f"   ✅ Data recolha: {start_date}", flush=True)
    time.sleep(0.5)
    
    # Data de devolução
    driver.execute_script("""
        const fechaDev = document.querySelector('input[id="fechaDevolucion"]');
        if (fechaDev) {
            fechaDev.value = arguments[0];
            fechaDev.dispatchEvent(new Event('input', {bubbles: true}));
            fechaDev.dispatchEvent(new Event('change', {bubbles: true}));
        }
    """, end_date)
    print(f"   ✅ Data devolução: {end_date}", flush=True)
    time.sleep(0.5)
    
    print("\n6️⃣  Preenchendo horas: 15:30...", flush=True)
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
    """, hora)
    print(f"   ✅ Horas: {hora}", flush=True)
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
        print("\n8️⃣  Submetendo...", flush=True)
        driver.execute_script("document.querySelector('form').submit();")
        time.sleep(5)
        
        url = driver.current_url
        print(f"\n📄 URL: {url}", flush=True)
        
        if "/do/list/" in url:
            print("\n🎉 SUCESSO!", flush=True)
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
