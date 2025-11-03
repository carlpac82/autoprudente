#!/usr/bin/env python3
"""
Teste FINAL com máquina de estados
Sabe sempre onde está e retoma após cookies
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
print("TESTE FINAL - MÁQUINA DE ESTADOS COM RETRY", flush=True)
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
    print("\n📍 ESTADO 1: Abrir página", flush=True)
    driver.get("https://www.carjet.com/aluguel-carros/index.htm")
    time.sleep(2)
    accept_cookies_if_present("(inicial)")
    time.sleep(1)
    
    print("\n📍 ESTADO 2: Preencher local", flush=True)
    pickup = driver.find_element(By.ID, "pickup")
    pickup.clear()
    pickup.send_keys("Albufeira Cidade")
    time.sleep(2)
    
    print("\n📍 ESTADO 3: Clicar dropdown COM RETRY", flush=True)
    clicked = False
    for attempt in range(2):
        if clicked:
            break
        print(f"   Tentativa {attempt + 1}/2", flush=True)
        try:
            dropdown_item = WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "#recogida_lista li[data-id='Albufeira Cidade'] a"))
            )
            dropdown_item.click()
            clicked = True
            print(f"   ✅ Clicado!", flush=True)
        except:
            result = driver.execute_script("""
                const item = document.querySelector('#recogida_lista li[data-id="Albufeira Cidade"]');
                if (item) { item.click(); return true; }
                return false;
            """)
            if result:
                clicked = True
                print(f"   ✅ Clicado via JS!", flush=True)
        
        if not clicked and attempt < 1:
            print(f"   🍪 Verificando cookies...", flush=True)
            if accept_cookies_if_present("(bloqueando dropdown)"):
                time.sleep(1)
                try:
                    pickup.click()
                    time.sleep(0.5)
                except:
                    pass
    
    time.sleep(1)
    accept_cookies_if_present("(após dropdown)")
    
    print("\n📍 ESTADO 4: Preencher datas COM RETRY", flush=True)
    dates_filled = False
    
    for date_attempt in range(3):
        if dates_filled:
            break
        
        print(f"   Tentativa {date_attempt + 1}/3", flush=True)
        
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
                horaEntrega: h2_ok,
                allFilled: r1 && r2 && r3 && h1_ok && h2_ok
            };
        """, 
        "Albufeira Cidade",
        start_dt.strftime("%d/%m/%Y"),
        end_dt.strftime("%d/%m/%Y")
        )
        
        print(f"   Resultado: {result}", flush=True)
        
        if result and result.get('allFilled'):
            dates_filled = True
            print(f"   ✅ Tudo preenchido!", flush=True)
        else:
            print(f"   ⚠️  Incompleto", flush=True)
            if date_attempt < 2:
                print(f"   🍪 Verificando cookies...", flush=True)
                if accept_cookies_if_present("(durante preenchimento)"):
                    time.sleep(1)
                    print(f"   🔄 Retomando preenchimento...", flush=True)
                else:
                    time.sleep(0.5)
    
    if not dates_filled:
        print(f"   ❌ Não preencheu tudo após 3 tentativas", flush=True)
    
    time.sleep(1)
    accept_cookies_if_present("(antes de submeter)")
    
    print("\n📍 ESTADO 5: Submeter formulário", flush=True)
    driver.execute_script("document.querySelector('form').submit();")
    time.sleep(5)
    accept_cookies_if_present("(após submeter)")
    time.sleep(2)
    
    url = driver.current_url
    print(f"\n📄 URL final: {url}", flush=True)
    
    if "/do/list/" in url:
        print("\n✅ SUCESSO! Chegou nos resultados!", flush=True)
        articles = driver.find_elements(By.CSS_SELECTOR, "section.newcarlist article")
        print(f"🚗 Encontrados {len(articles)} carros", flush=True)
        
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
    
    print("\n" + "=" * 80, flush=True)
    print("✅ TESTE CONCLUÍDO! Chrome aberto 90 segundos", flush=True)
    print("=" * 80, flush=True)
    
    time.sleep(90)
    
except Exception as e:
    print(f"\n❌ ERRO: {e}", flush=True)
    import traceback
    traceback.print_exc()
    time.sleep(30)
finally:
    driver.quit()
    print("\n👋 Chrome fechado", flush=True)
