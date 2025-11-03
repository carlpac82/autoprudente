#!/usr/bin/env python3
"""
Teste replicando EXATAMENTE o que você fez manualmente
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
print("TESTE - REPLICANDO PROCESSO MANUAL", flush=True)
print("=" * 80, flush=True)

start_dt = datetime.now() + timedelta(days=7)
end_dt = start_dt + timedelta(days=5)

print(f"\nDatas:", flush=True)
print(f"  Recolha: {start_dt.strftime('%d %b, %H:%M')}", flush=True)
print(f"  Devolução: {end_dt.strftime('%d %b, %H:%M')}", flush=True)

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
    
    print("\n2️⃣  Rejeitando cookies...", flush=True)
    # Tentar rejeitar cookies
    try:
        driver.execute_script("""
            const buttons = document.querySelectorAll('button, a');
            for (let btn of buttons) {
                const text = btn.textContent.toLowerCase();
                if (text.includes('rejeitar') || text.includes('reject') || text.includes('recusar')) {
                    btn.click();
                    console.log('Cookies rejeitados');
                    break;
                }
            }
        """)
        print("   ✅ Cookies rejeitados", flush=True)
    except:
        print("   ℹ️  Sem cookies ou já removidos", flush=True)
    
    time.sleep(1)
    
    print("\n3️⃣  Preenchendo local: Albufeira Cidade...", flush=True)
    pickup = driver.find_element(By.ID, "pickup")
    pickup.clear()
    pickup.send_keys("Albufeira Cidade")
    print("   ✅ Digitado", flush=True)
    time.sleep(2)
    
    print("\n4️⃣  Clicando no dropdown...", flush=True)
    try:
        # Tentar clicar no item do dropdown
        dropdown_item = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#recogida_lista li[data-id='Albufeira Cidade']"))
        )
        dropdown_item.click()
        print("   ✅ Dropdown clicado (método 1)", flush=True)
    except:
        try:
            driver.execute_script("document.querySelector('#recogida_lista li[data-id=\"Albufeira Cidade\"]').click();")
            print("   ✅ Dropdown clicado (método 2)", flush=True)
        except:
            print("   ⚠️  Dropdown não encontrado", flush=True)
    
    time.sleep(2)
    
    print("\n5️⃣  Preenchendo datas...", flush=True)
    # Preencher data de recolha
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
    
    # Preencher data de devolução
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
    
    print("\n6️⃣  Preenchendo horas...", flush=True)
    # Usar horas fixas válidas (10:00)
    driver.execute_script("""
        const horaRec = document.querySelector('select[id="fechaRecogidaSelHour"]');
        const horaDev = document.querySelector('select[id="fechaDevolucionSelHour"]');
        if (horaRec) {
            horaRec.value = '10:00';
            horaRec.dispatchEvent(new Event('change', {bubbles: true}));
        }
        if (horaDev) {
            horaDev.value = '10:00';
            horaDev.dispatchEvent(new Event('change', {bubbles: true}));
        }
    """)
    print(f"   ✅ Hora recolha: 10:00", flush=True)
    print(f"   ✅ Hora devolução: 10:00", flush=True)
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
    
    if not all_ok:
        print("\n❌ CAMPOS VAZIOS! Não submeter.", flush=True)
    else:
        print("\n8️⃣  Clicando em Pesquisar...", flush=True)
        
        # Tentar encontrar botão de pesquisa
        try:
            # Método 1: Por texto
            button = driver.find_element(By.XPATH, "//button[contains(text(), 'Pesquisar')]")
            button.click()
            print("   ✅ Botão 'Pesquisar' clicado", flush=True)
        except:
            try:
                # Método 2: Submit button
                button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
                button.click()
                print("   ✅ Botão submit clicado", flush=True)
            except:
                # Método 3: Form submit
                driver.execute_script("document.querySelector('form').submit();")
                print("   ✅ Form submetido", flush=True)
        
        print("\n⏳ Aguardando resultados...", flush=True)
        time.sleep(5)
        
        url = driver.current_url
        print(f"\n📄 URL final: {url}", flush=True)
        
        if "/do/list/" in url:
            print("\n🎉 SUCESSO TOTAL!", flush=True)
            articles = driver.find_elements(By.CSS_SELECTOR, "section.newcarlist article")
            print(f"🚗 {len(articles)} carros encontrados", flush=True)
            
            if len(articles) > 0:
                print("\n📊 Primeiros 3:", flush=True)
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
