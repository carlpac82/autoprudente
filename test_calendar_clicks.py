#!/usr/bin/env python3
"""
Teste: CLICAR no calendário e dropdown (não digitar!)
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
print("TESTE - CLICAR CALENDÁRIO E DROPDOWN", flush=True)
print("=" * 80, flush=True)

start_dt = datetime.now() + timedelta(days=7)
end_dt = start_dt + timedelta(days=5)

print(f"\nDatas alvo:", flush=True)
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

try:
    print("\n1️⃣  Abrindo página...", flush=True)
    driver.get("https://www.carjet.com/aluguel-carros/index.htm")
    time.sleep(2)
    
    # Remover cookies
    driver.execute_script("document.querySelectorAll('[id*=cookie]').forEach(el => el.remove());")
    time.sleep(1)
    
    print("\n2️⃣  Preenchendo local...", flush=True)
    pickup = driver.find_element(By.ID, "pickup")
    pickup.clear()
    pickup.send_keys("Albufeira Cidade")
    time.sleep(2)
    driver.execute_script("document.querySelector('#recogida_lista li[data-id=\"Albufeira Cidade\"]').click();")
    print("   ✅ Local selecionado", flush=True)
    time.sleep(2)
    
    print("\n3️⃣  Clicando no campo de DATA DE RECOLHA para abrir calendário...", flush=True)
    try:
        fecha_rec_input = driver.find_element(By.ID, "fechaRecogida")
        fecha_rec_input.click()
        print("   ✅ Calendário de recolha aberto", flush=True)
        time.sleep(1)
        
        # Procurar e clicar na data no calendário
        print(f"   🗓️  Procurando dia {start_dt.day}...", flush=True)
        # Tentar clicar no dia específico
        day_selector = f"//td[@data-day='{start_dt.day}' and @data-month='{start_dt.month - 1}']"
        try:
            day_cell = driver.find_element(By.XPATH, day_selector)
            day_cell.click()
            print(f"   ✅ Dia {start_dt.day} clicado", flush=True)
        except:
            print(f"   ⚠️  Não encontrou dia específico, tentando alternativa...", flush=True)
            # Alternativa: clicar em qualquer dia disponível
            driver.execute_script("""
                const days = document.querySelectorAll('.ui-datepicker-calendar td:not(.ui-datepicker-unselectable) a');
                if (days.length > 0) days[7].click(); // Clicar no 8º dia disponível
            """)
        
        time.sleep(1)
    except Exception as e:
        print(f"   ❌ Erro ao abrir calendário: {e}", flush=True)
    
    print("\n4️⃣  Clicando no campo de DATA DE DEVOLUÇÃO...", flush=True)
    try:
        fecha_dev_input = driver.find_element(By.ID, "fechaDevolucion")
        fecha_dev_input.click()
        print("   ✅ Calendário de devolução aberto", flush=True)
        time.sleep(1)
        
        print(f"   🗓️  Procurando dia {end_dt.day}...", flush=True)
        day_selector = f"//td[@data-day='{end_dt.day}' and @data-month='{end_dt.month - 1}']"
        try:
            day_cell = driver.find_element(By.XPATH, day_selector)
            day_cell.click()
            print(f"   ✅ Dia {end_dt.day} clicado", flush=True)
        except:
            driver.execute_script("""
                const days = document.querySelectorAll('.ui-datepicker-calendar td:not(.ui-datepicker-unselectable) a');
                if (days.length > 0) days[12].click(); // Clicar no 13º dia disponível
            """)
        
        time.sleep(1)
    except Exception as e:
        print(f"   ❌ Erro: {e}", flush=True)
    
    print("\n5️⃣  Selecionando HORA DE RECOLHA no dropdown...", flush=True)
    try:
        hora_rec_select = driver.find_element(By.ID, "fechaRecogidaSelHour")
        hora_rec_select.click()
        time.sleep(0.5)
        # Selecionar 10:00
        driver.execute_script("""
            const select = document.querySelector('select[id="fechaRecogidaSelHour"]');
            select.value = '10:00';
            select.dispatchEvent(new Event('change', {bubbles: true}));
        """)
        print("   ✅ Hora 10:00 selecionada", flush=True)
        time.sleep(0.5)
    except Exception as e:
        print(f"   ❌ Erro: {e}", flush=True)
    
    print("\n6️⃣  Selecionando HORA DE DEVOLUÇÃO no dropdown...", flush=True)
    try:
        hora_dev_select = driver.find_element(By.ID, "fechaDevolucionSelHour")
        hora_dev_select.click()
        time.sleep(0.5)
        driver.execute_script("""
            const select = document.querySelector('select[id="fechaDevolucionSelHour"]');
            select.value = '10:00';
            select.dispatchEvent(new Event('change', {bubbles: true}));
        """)
        print("   ✅ Hora 10:00 selecionada", flush=True)
        time.sleep(0.5)
    except Exception as e:
        print(f"   ❌ Erro: {e}", flush=True)
    
    print("\n7️⃣  Verificando valores finais...", flush=True)
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
        print("\n8️⃣  Clicando Pesquisar...", flush=True)
        driver.execute_script("document.querySelector('form').submit();")
        time.sleep(5)
        
        url = driver.current_url
        print(f"\n📄 URL: {url}", flush=True)
        
        if "/do/list/" in url:
            print("\n🎉 SUCESSO!", flush=True)
            articles = driver.find_elements(By.CSS_SELECTOR, "section.newcarlist article")
            print(f"🚗 {len(articles)} carros", flush=True)
        elif "war=" in url:
            war = url.split("war=")[1].split("&")[0]
            print(f"\n❌ ERRO: war={war}", flush=True)
    else:
        print("\n❌ Campos vazios!", flush=True)
    
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
