#!/usr/bin/env python3
"""
Teste com RETRY após aceitar cookies
Simula: clicar dropdown → cookie aparece → aceita → RETOMA dropdown
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
print("TESTE COM RETRY APÓS COOKIES", flush=True)
print("=" * 80, flush=True)

start_dt = datetime.now() + timedelta(days=7)
end_dt = start_dt + timedelta(days=5)

chrome_options = Options()
chrome_options.add_argument('--start-maximized')

print("\n🚀 Iniciando Chrome...", flush=True)
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

def accept_cookies_if_present(step_name=""):
    """Aceita cookies e retorna True se encontrou"""
    try:
        result = driver.execute_script("""
            const buttons = document.querySelectorAll('button');
            let found = false;
            for (let btn of buttons) {
                const text = btn.textContent.toLowerCase().trim();
                if (text.includes('aceitar todos') || text.includes('aceitar tudo')) {
                    btn.click();
                    console.log('✓ Cookies aceitos');
                    found = true;
                    break;
                }
            }
            document.querySelectorAll('[id*=cookie], [class*=cookie], [id*=didomi], [class*=didomi]').forEach(el => {
                el.remove();
            });
            return found;
        """)
        if result:
            print(f"   ✅ Cookies aceitos {step_name}", flush=True)
        return result
    except:
        return False

try:
    print("\n1️⃣  Abrindo página...", flush=True)
    driver.get("https://www.carjet.com/aluguel-carros/index.htm")
    time.sleep(2)
    accept_cookies_if_present("(inicial)")
    time.sleep(1)
    
    print("\n2️⃣  Preenchendo local...", flush=True)
    pickup = driver.find_element(By.ID, "pickup")
    pickup.clear()
    pickup.send_keys("Albufeira Cidade")
    time.sleep(2)
    
    print("\n3️⃣  Clicando no dropdown COM RETRY...", flush=True)
    clicked = False
    max_attempts = 2
    
    for attempt in range(max_attempts):
        if clicked:
            break
        
        print(f"   Tentativa {attempt + 1}/{max_attempts}", flush=True)
        
        # Tentar clicar
        try:
            dropdown_item = WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "#recogida_lista li[data-id='Albufeira Cidade'] a"))
            )
            dropdown_item.click()
            clicked = True
            print(f"   ✅ Dropdown clicado!", flush=True)
            time.sleep(1)
        except:
            # Tentar via JS
            try:
                result = driver.execute_script("""
                    const item = document.querySelector('#recogida_lista li[data-id="Albufeira Cidade"]');
                    if (item) {
                        item.click();
                        return true;
                    }
                    return false;
                """)
                if result:
                    clicked = True
                    print(f"   ✅ Dropdown clicado via JS!", flush=True)
                    time.sleep(1)
            except:
                pass
        
        # Se não clicou, verificar cookies
        if not clicked and attempt < max_attempts - 1:
            print(f"   ⚠️  Não clicou. Verificando cookies...", flush=True)
            cookies_found = accept_cookies_if_present("(bloqueando)")
            if cookies_found:
                time.sleep(1)
                # Reabrir dropdown
                print(f"   🔄 Reabrindo dropdown...", flush=True)
                try:
                    pickup.click()
                    time.sleep(0.5)
                except:
                    pass
    
    if not clicked:
        print(f"   ❌ Não conseguiu clicar após {max_attempts} tentativas", flush=True)
    
    accept_cookies_if_present("(após dropdown)")
    time.sleep(1)
    
    print("\n4️⃣  Preenchendo datas e horas...", flush=True)
    driver.execute_script("""
        function fill(sel, val) {
            const el = document.querySelector(sel);
            if (el) { 
                el.value = val;
                el.dispatchEvent(new Event('change', {bubbles: true}));
                return true;
            }
            return false;
        }
        fill('input[name="dropoff"]', arguments[0]);
        fill('input[name="fechaRecogida"]', arguments[1]);
        fill('input[name="fechaEntrega"]', arguments[2]);
        const h1 = document.querySelector('select[name="fechaRecogidaSelHour"]');
        const h2 = document.querySelector('select[name="fechaEntregaSelHour"]');
        if (h1) h1.value = '10:00';
        if (h2) h2.value = '10:00';
    """, 
    "Albufeira Cidade",
    start_dt.strftime("%d/%m/%Y"),
    end_dt.strftime("%d/%m/%Y")
    )
    print("   ✅ Datas preenchidas", flush=True)
    time.sleep(1)
    
    # Verificar valores
    print("\n🔍 Verificando formulário...", flush=True)
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
    for key, val in values.items():
        print(f"   {key}: '{val}'", flush=True)
    
    accept_cookies_if_present("(antes de submeter)")
    
    print("\n5️⃣  Submetendo formulário...", flush=True)
    driver.execute_script("document.querySelector('form').submit();")
    time.sleep(5)
    accept_cookies_if_present("(após submeter)")
    time.sleep(2)
    
    url = driver.current_url
    print(f"\n📄 URL final: {url}", flush=True)
    
    if "/do/list/" in url:
        print("✅ SUCESSO! Chegou nos resultados!", flush=True)
        articles = driver.find_elements(By.CSS_SELECTOR, "section.newcarlist article")
        print(f"🚗 {len(articles)} carros", flush=True)
    elif "war=" in url:
        war = url.split("war=")[1].split("&")[0]
        print(f"❌ ERRO: war={war}", flush=True)
    else:
        print(f"⚠️  URL inesperada", flush=True)
    
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
