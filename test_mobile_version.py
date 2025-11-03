#!/usr/bin/env python3
"""
Teste com versão MOBILE do Carjet
Pode ter menos popups de cookies
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
print("TESTE - VERSÃO MOBILE DO CARJET", flush=True)
print("=" * 80, flush=True)

start_dt = datetime.now() + timedelta(days=7)
end_dt = start_dt + timedelta(days=5)

# Configurar Chrome como MOBILE
chrome_options = Options()
chrome_options.add_argument('--start-maximized')

# User-Agent de iPhone
mobile_user_agent = "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1"
chrome_options.add_argument(f'user-agent={mobile_user_agent}')

# Emular dispositivo móvel
mobile_emulation = {
    "deviceMetrics": { "width": 375, "height": 812, "pixelRatio": 3.0 },
    "userAgent": mobile_user_agent
}
chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)

print("\n🚀 Iniciando Chrome em modo MOBILE...", flush=True)
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

def accept_cookies():
    try:
        result = driver.execute_script("""
            const buttons = document.querySelectorAll('button');
            for (let btn of buttons) {
                const text = btn.textContent.toLowerCase().trim();
                if (text.includes('aceitar') || text.includes('accept')) {
                    btn.click();
                    console.log('Cookie aceite:', btn.textContent);
                    return true;
                }
            }
            return false;
        """)
        if result:
            print("   ✅ Cookie aceite", flush=True)
        return result
    except:
        return False

try:
    print("\n1️⃣  Abrindo versão mobile...", flush=True)
    driver.get("https://www.carjet.com/aluguel-carros/index.htm")
    time.sleep(3)
    accept_cookies()
    time.sleep(1)
    
    print(f"\n📱 Tamanho da janela: {driver.get_window_size()}", flush=True)
    print(f"📱 User-Agent: {driver.execute_script('return navigator.userAgent')[:80]}...", flush=True)
    
    print("\n2️⃣  Procurando campos no mobile...", flush=True)
    
    # Verificar que campos existem
    fields = driver.execute_script("""
        const inputs = Array.from(document.querySelectorAll('input[type="text"], input[type="date"]'));
        const selects = Array.from(document.querySelectorAll('select'));
        
        return {
            inputs: inputs.map(i => ({id: i.id, name: i.name, placeholder: i.placeholder})),
            selects: selects.map(s => ({id: s.id, name: s.name})),
            hasPickup: !!document.querySelector('input[id="pickup"]'),
            hasFechaRecogida: !!document.querySelector('input[id="fechaRecogida"]'),
            hasFechaDevolucion: !!document.querySelector('input[id="fechaDevolucion"]')
        };
    """)
    
    print(f"\n📋 Campos encontrados:", flush=True)
    print(f"   Pickup: {fields['hasPickup']}", flush=True)
    print(f"   FechaRecogida: {fields['hasFechaRecogida']}", flush=True)
    print(f"   FechaDevolucion: {fields['hasFechaDevolucion']}", flush=True)
    print(f"   Total inputs: {len(fields['inputs'])}", flush=True)
    print(f"   Total selects: {len(fields['selects'])}", flush=True)
    
    print("\n3️⃣  Preenchendo local...", flush=True)
    try:
        pickup = driver.find_element(By.ID, "pickup")
        pickup.clear()
        pickup.send_keys("Albufeira Cidade")
        print("   ✅ Local digitado", flush=True)
        time.sleep(2)
        
        # Tentar clicar no dropdown
        try:
            driver.execute_script("document.querySelector('#recogida_lista li[data-id=\"Albufeira Cidade\"]').click();")
            print("   ✅ Dropdown clicado", flush=True)
        except:
            print("   ⚠️  Dropdown não encontrado (pode ser diferente no mobile)", flush=True)
        
        time.sleep(1)
        accept_cookies()
        
    except Exception as e:
        print(f"   ❌ Erro: {e}", flush=True)
    
    print("\n4️⃣  Preenchendo datas...", flush=True)
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
    
    print(f"   Resultado: {result}", flush=True)
    time.sleep(1)
    accept_cookies()
    
    print("\n5️⃣  Verificando valores...", flush=True)
    values = driver.execute_script("""
        return {
            pickup: document.querySelector('input[id="pickup"]')?.value || 'VAZIO',
            fechaRecogida: document.querySelector('input[id="fechaRecogida"]')?.value || 'VAZIO',
            fechaDevolucion: document.querySelector('input[id="fechaDevolucion"]')?.value || 'VAZIO',
            horaRecogida: document.querySelector('select[id="fechaRecogidaSelHour"]')?.value || 'VAZIO',
            horaDevolucion: document.querySelector('select[id="fechaDevolucionSelHour"]')?.value || 'VAZIO'
        };
    """)
    
    for key, val in values.items():
        status = "✅" if val != 'VAZIO' else "❌"
        print(f"   {status} {key}: {val}", flush=True)
    
    all_ok = all(v != 'VAZIO' for v in values.values())
    
    if all_ok:
        print("\n6️⃣  Submetendo...", flush=True)
        driver.execute_script("document.querySelector('form').submit();")
        time.sleep(5)
        accept_cookies()
        time.sleep(2)
        
        url = driver.current_url
        print(f"\n📄 URL: {url}", flush=True)
        
        if "/do/list/" in url:
            print("🎉 SUCESSO!", flush=True)
            articles = driver.find_elements(By.CSS_SELECTOR, "section.newcarlist article, .car-item, .result-item")
            print(f"🚗 {len(articles)} resultados", flush=True)
        elif "war=" in url:
            war = url.split("war=")[1].split("&")[0]
            print(f"❌ ERRO: war={war}", flush=True)
    else:
        print("\n❌ Campos vazios, não submeter", flush=True)
    
    print("\n⏱️  Chrome mobile aberto 90 segundos", flush=True)
    time.sleep(90)
    
except Exception as e:
    print(f"\n❌ ERRO: {e}", flush=True)
    import traceback
    traceback.print_exc()
    time.sleep(30)
finally:
    driver.quit()
    print("\n👋 Fechado", flush=True)
