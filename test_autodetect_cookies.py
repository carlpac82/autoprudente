#!/usr/bin/env python3
"""
Teste com AUTODETECÇÃO de cookies em cada passo
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
print("TESTE COM AUTODETECÇÃO DE COOKIES", flush=True)
print("=" * 80, flush=True)

# Datas
start_dt = datetime.now() + timedelta(days=7)
end_dt = start_dt + timedelta(days=5)

chrome_options = Options()
chrome_options.add_argument('--start-maximized')
chrome_options.add_argument('--disable-blink-features=AutomationControlled')

print("\n🚀 Iniciando Chrome...", flush=True)
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# FUNÇÃO HELPER: Autodetectar cookies
def accept_cookies_if_present(step_name=""):
    """Detecta e aceita cookies automaticamente"""
    try:
        result = driver.execute_script("""
            const buttons = document.querySelectorAll('button');
            let found = false;
            for (let btn of buttons) {
                const text = btn.textContent.toLowerCase().trim();
                if (text.includes('aceitar todos') || text.includes('aceitar tudo') || 
                    text.includes('accept all') || text.includes('aceptar todo')) {
                    btn.click();
                    console.log('✓ Cookies aceitos:', btn.textContent);
                    found = true;
                    break;
                }
            }
            document.querySelectorAll('[id*=cookie], [class*=cookie], [id*=didomi], [class*=didomi]').forEach(el => {
                el.remove();
            });
            document.body.style.overflow = 'auto';
            return found;
        """)
        if result:
            print(f"   ✅ Cookies aceitos {step_name}", flush=True)
        else:
            print(f"   ℹ️  Sem cookies {step_name}", flush=True)
        return result
    except Exception as e:
        print(f"   ⚠️  Erro {step_name}: {e}", flush=True)
        return False

try:
    print("\n📍 PASSO 1: Abrindo página...", flush=True)
    driver.get("https://www.carjet.com/aluguel-carros/index.htm")
    time.sleep(2)
    print("✅ Página aberta", flush=True)
    
    print("\n🍪 PASSO 2: Autodetectando cookies iniciais...", flush=True)
    time.sleep(0.5)
    accept_cookies_if_present("(inicial)")
    time.sleep(1)
    
    print("\n📝 PASSO 3: Preenchendo local...", flush=True)
    pickup = driver.find_element(By.ID, "pickup")
    pickup.clear()
    pickup.send_keys("Albufeira Cidade")
    time.sleep(2)
    
    # Clicar dropdown
    try:
        dropdown_item = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#recogida_lista li[data-id='Albufeira Cidade'] a"))
        )
        dropdown_item.click()
        print("✅ Dropdown clicado", flush=True)
    except:
        driver.execute_script("document.querySelector('#recogida_lista li[data-id=\"Albufeira Cidade\"]').click();")
        print("✅ Dropdown clicado via JS", flush=True)
    time.sleep(1)
    
    print("\n🍪 Autodetectando cookies após dropdown...", flush=True)
    accept_cookies_if_present("(após dropdown)")
    time.sleep(0.5)
    
    print("\n📅 PASSO 4: Preenchendo datas e horas...", flush=True)
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
    print("✅ Datas preenchidas", flush=True)
    time.sleep(1)
    
    print("\n🍪 Autodetectando cookies antes de submeter...", flush=True)
    accept_cookies_if_present("(antes de submeter)")
    
    print("\n🔍 PASSO 5: Submetendo formulário...", flush=True)
    driver.execute_script("document.querySelector('form').submit();")
    print("✅ Formulário submetido", flush=True)
    
    print("\n⏳ Aguardando 5 segundos...", flush=True)
    time.sleep(5)
    
    print("\n🍪 Autodetectando cookies APÓS submeter (IMPORTANTE!)...", flush=True)
    accept_cookies_if_present("(após submeter)")
    time.sleep(2)
    
    url = driver.current_url
    print(f"\n📄 URL final: {url}", flush=True)
    
    if "/do/list/" in url:
        print("✅ SUCESSO! Chegou nos resultados!", flush=True)
        articles = driver.find_elements(By.CSS_SELECTOR, "section.newcarlist article")
        print(f"🚗 Encontrados {len(articles)} carros", flush=True)
        
        if len(articles) > 0:
            print("\n📊 Primeiros 3 resultados:", flush=True)
            for i, art in enumerate(articles[:3], 1):
                try:
                    car = art.find_element(By.CSS_SELECTOR, "h2").text
                    price = art.find_element(By.CSS_SELECTOR, ".pr-euros").text
                    print(f"  {i}. {car} - {price}", flush=True)
                except:
                    print(f"  {i}. [Erro]", flush=True)
    else:
        print("❌ NÃO chegou nos resultados", flush=True)
        print(f"   URL: {url}", flush=True)
    
    print("\n" + "=" * 80, flush=True)
    print("✅ TESTE CONCLUÍDO! Chrome fica aberto 60 segundos", flush=True)
    print("=" * 80, flush=True)
    
    time.sleep(60)
    
except Exception as e:
    print(f"\n❌ ERRO: {e}", flush=True)
    import traceback
    traceback.print_exc()
    time.sleep(30)
finally:
    driver.quit()
    print("\n👋 Chrome fechado", flush=True)
