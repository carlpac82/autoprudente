#!/usr/bin/env python3
"""
Teste: Ordem correta - Local PRIMEIRO, depois Datas e Horas
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
print("TESTE - ORDEM CORRETA: LOCAL → DATAS → HORAS", flush=True)
print("=" * 80, flush=True)

start_dt = datetime.now() + timedelta(days=7)
end_dt = start_dt + timedelta(days=5)

print(f"\nDatas esperadas:", flush=True)
print(f"  Recolha: {start_dt.strftime('%d/%m/%Y')} às 10:00", flush=True)
print(f"  Devolução: {end_dt.strftime('%d/%m/%Y')} às 10:00", flush=True)

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
    try:
        driver.execute_script("""
            document.querySelectorAll('[id*=cookie], [class*=cookie]').forEach(el => el.remove());
        """)
    except:
        pass

try:
    print("\n1️⃣  Abrindo página...", flush=True)
    driver.get("https://www.carjet.com/aluguel-carros/index.htm")
    time.sleep(1)
    reject_cookies()
    time.sleep(0.5)
    
    print("\n2️⃣  Preenchendo LOCAL...", flush=True)
    pickup = driver.find_element(By.ID, "pickup")
    pickup.clear()
    pickup.send_keys("Albufeira Cidade")
    time.sleep(2)
    driver.execute_script("document.querySelector('#recogida_lista li[data-id=\"Albufeira Cidade\"]').click();")
    print("   ✅ Local selecionado: Albufeira Cidade", flush=True)
    time.sleep(1)
    reject_cookies()
    time.sleep(0.5)
    
    print("\n3️⃣  Preenchendo DATAS...", flush=True)
    # Limpar e preencher data de recolha
    driver.execute_script("""
        const r = document.querySelector('input[id="fechaRecogida"]');
        if (r) {
            r.value = '';
            r.value = arguments[0];
            r.dispatchEvent(new Event('input', {bubbles: true}));
            r.dispatchEvent(new Event('change', {bubbles: true}));
        }
    """, start_dt.strftime("%d/%m/%Y"))
    print(f"   ✅ Data recolha: {start_dt.strftime('%d/%m/%Y')}", flush=True)
    time.sleep(0.5)
    
    # Limpar e preencher data de devolução
    driver.execute_script("""
        const d = document.querySelector('input[id="fechaDevolucion"]');
        if (d) {
            d.value = '';
            d.value = arguments[0];
            d.dispatchEvent(new Event('input', {bubbles: true}));
            d.dispatchEvent(new Event('change', {bubbles: true}));
        }
    """, end_dt.strftime("%d/%m/%Y"))
    print(f"   ✅ Data devolução: {end_dt.strftime('%d/%m/%Y')}", flush=True)
    time.sleep(0.5)
    reject_cookies()
    
    print("\n4️⃣  Preenchendo HORAS...", flush=True)
    driver.execute_script("""
        const h1 = document.querySelector('select[id="fechaRecogidaSelHour"]');
        const h2 = document.querySelector('select[id="fechaDevolucionSelHour"]');
        if (h1) {
            h1.value = '10:00';
            h1.dispatchEvent(new Event('change', {bubbles: true}));
        }
        if (h2) {
            h2.value = '10:00';
            h2.dispatchEvent(new Event('change', {bubbles: true}));
        }
    """)
    print(f"   ✅ Hora recolha: 10:00", flush=True)
    print(f"   ✅ Hora devolução: 10:00", flush=True)
    time.sleep(0.5)
    reject_cookies()
    
    print("\n5️⃣  Verificando valores FINAIS...", flush=True)
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
    
    if not all_ok:
        print("\n❌ CAMPOS VAZIOS! Não submeter.", flush=True)
    else:
        print("\n✅ Todos os campos preenchidos corretamente!", flush=True)
        reject_cookies()
        
        print("\n6️⃣  Clicando PESQUISAR...", flush=True)
        try:
            button = driver.find_element(By.XPATH, "//button[contains(text(), 'Pesquisar')]")
            button.click()
            print("   ✅ Botão clicado", flush=True)
        except:
            driver.execute_script("document.querySelector('button[type=\"submit\"]').click();")
            print("   ✅ Submit clicado", flush=True)
        
        time.sleep(5)
        reject_cookies()
        time.sleep(2)
        
        url = driver.current_url
        print(f"\n📄 URL: {url}", flush=True)
        
        if "/do/list/" in url:
            print("\n🎉 SUCESSO TOTAL!", flush=True)
            articles = driver.find_elements(By.CSS_SELECTOR, "section.newcarlist article")
            print(f"🚗 {len(articles)} carros encontrados", flush=True)
            
            if len(articles) > 0:
                print("\n📊 Primeiros 3 carros:", flush=True)
                for i, art in enumerate(articles[:3], 1):
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
