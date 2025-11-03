#!/usr/bin/env python3
"""
Teste: Verificar campos preenchidos e CLICAR no botão Pesquisar
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
print("TESTE - VERIFICAR E CLICAR PESQUISAR", flush=True)
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
    try:
        driver.execute_script("""
            document.querySelectorAll('button, a, [role="button"]').forEach(btn => {
                const text = btn.textContent.toLowerCase();
                if (text.includes('rejeitar') || text.includes('reject')) {
                    btn.click();
                }
            });
            document.querySelectorAll('[id*=cookie], [class*=cookie]').forEach(el => el.remove());
        """)
    except:
        pass

def fill_form():
    """Preenche formulário completo"""
    print("   📝 Preenchendo formulário...", flush=True)
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
    return result

def verify_form():
    """Verifica se formulário está preenchido"""
    values = driver.execute_script("""
        return {
            pickup: document.querySelector('input[id="pickup"]')?.value || '',
            fechaRecogida: document.querySelector('input[id="fechaRecogida"]')?.value || '',
            fechaDevolucion: document.querySelector('input[id="fechaDevolucion"]')?.value || '',
            horaRecogida: document.querySelector('select[id="fechaRecogidaSelHour"]')?.value || '',
            horaDevolucion: document.querySelector('select[id="fechaDevolucionSelHour"]')?.value || ''
        };
    """)
    all_filled = all(v != '' for v in values.values())
    return all_filled, values

try:
    print("\n1️⃣  Abrindo página...", flush=True)
    driver.get("https://www.carjet.com/aluguel-carros/index.htm")
    time.sleep(1)
    reject_cookies()
    time.sleep(0.5)
    
    print("\n2️⃣  Preenchendo local...", flush=True)
    pickup = driver.find_element(By.ID, "pickup")
    pickup.clear()
    pickup.send_keys("Albufeira Cidade")
    time.sleep(2)
    driver.execute_script("document.querySelector('#recogida_lista li[data-id=\"Albufeira Cidade\"]').click();")
    print("   ✅ Local selecionado", flush=True)
    time.sleep(1)
    reject_cookies()
    
    print("\n3️⃣  Preenchendo formulário COM VERIFICAÇÃO...", flush=True)
    max_attempts = 3
    
    for attempt in range(max_attempts):
        print(f"\n   Tentativa {attempt + 1}/{max_attempts}", flush=True)
        
        # Preencher
        fill_form()
        time.sleep(0.5)
        
        # Verificar
        filled, values = verify_form()
        
        if filled:
            print(f"   ✅ TUDO PREENCHIDO!", flush=True)
            for key, val in values.items():
                print(f"      {key}: {val}", flush=True)
            break
        else:
            print(f"   ⚠️  Incompleto:", flush=True)
            for key, val in values.items():
                status = "✅" if val else "❌"
                print(f"      {status} {key}: {val or 'VAZIO'}", flush=True)
            
            if attempt < max_attempts - 1:
                print(f"   🔄 Rejeitando cookies e tentando novamente...", flush=True)
                reject_cookies()
                time.sleep(1)
    
    # Verificação final
    print("\n4️⃣  Verificação FINAL antes de clicar...", flush=True)
    filled, values = verify_form()
    
    if not filled:
        print("   ❌ CAMPOS VAZIOS! Não clicar.", flush=True)
        for key, val in values.items():
            print(f"      {key}: {val or 'VAZIO'}", flush=True)
    else:
        print("   ✅ Tudo OK!", flush=True)
        reject_cookies()
        
        print("\n5️⃣  Clicando no botão PESQUISAR...", flush=True)
        
        # Tentar encontrar e clicar no botão Pesquisar
        try:
            # Método 1: Por texto
            button = driver.find_element(By.XPATH, "//button[contains(text(), 'Pesquisar')]")
            button.click()
            print("   ✅ Botão clicado (método 1)", flush=True)
        except:
            try:
                # Método 2: Por tipo submit
                driver.execute_script("""
                    const btn = document.querySelector('button[type="submit"]');
                    if (btn) btn.click();
                """)
                print("   ✅ Botão clicado (método 2)", flush=True)
            except:
                # Método 3: Submit do form
                driver.execute_script("document.querySelector('form').submit();")
                print("   ✅ Form submetido (método 3)", flush=True)
        
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
            print("   Os campos provavelmente ficaram vazios!", flush=True)
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
