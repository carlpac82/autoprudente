#!/usr/bin/env python3
"""
Teste com TODOS os 4 dispositivos
"""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import datetime, timedelta

# TODOS OS DISPOSITIVOS
mobile_devices = [
    {
        'name': 'iPhone 13',
        'ua': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1',
        'width': 390, 'height': 844, 'pixelRatio': 3.0
    },
    {
        'name': 'iPhone 12',
        'ua': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1',
        'width': 390, 'height': 844, 'pixelRatio': 3.0
    },
    {
        'name': 'Samsung Galaxy S21',
        'ua': 'Mozilla/5.0 (Linux; Android 12; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Mobile Safari/537.36',
        'width': 360, 'height': 800, 'pixelRatio': 3.0
    },
    {
        'name': 'Google Pixel 5',
        'ua': 'Mozilla/5.0 (Linux; Android 11; Pixel 5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Mobile Safari/537.36',
        'width': 393, 'height': 851, 'pixelRatio': 2.75
    }
]

url = "https://www.carjet.com/aluguel-carros/index.htm"
location = "Faro Aeroporto (FAO)"
start_date = datetime.now() + timedelta(days=7)
end_date = start_date + timedelta(days=3)

results = []

print("═" * 80)
print("🧪 TESTE COM TODOS OS 4 DISPOSITIVOS")
print("═" * 80)
print(f"📍 Local: {location}")
print(f"📅 Datas: {start_date.strftime('%d/%m/%Y')} - {end_date.strftime('%d/%m/%Y')}")
print(f"🔗 URL: {url}")
print("═" * 80)

for idx, device in enumerate(mobile_devices, 1):
    print(f"\n{'='*80}")
    print(f"📱 TESTE {idx}/4: {device['name']}")
    print(f"{'='*80}")
    print(f"   Resolução: {device['width']}x{device['height']}")
    print(f"   Pixel Ratio: {device['pixelRatio']}")
    
    # Configurar Chrome
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument(f'user-agent={device["ua"]}')
    
    # Emulação mobile
    mobile_emulation = {
        "deviceMetrics": { 
            "width": device['width'], 
            "height": device['height'], 
            "pixelRatio": device['pixelRatio']
        },
        "userAgent": device['ua']
    }
    chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
    
    # Anti-detecção
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    # Caminho do Chrome
    chrome_options.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    
    driver = webdriver.Chrome(options=chrome_options)
    
    # Esconder webdriver
    driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
        'source': '''
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
        '''
    })
    
    driver.set_page_load_timeout(20)
    
    try:
        start_time = time.time()
        
        # Navegar
        print(f"\n   🌐 Navegando...")
        driver.get(url)
        
        # Cookies
        time.sleep(0.5)
        driver.execute_script("""
            const buttons = document.querySelectorAll('button, a, [role="button"]');
            for (let btn of buttons) {
                const text = btn.textContent.toLowerCase().trim();
                if (text.includes('rejeitar') || text.includes('reject')) {
                    btn.click();
                    break;
                }
            }
        """)
        time.sleep(0.5)
        
        # Escrever local
        print(f"   ✏️  Escrevendo local...")
        pickup_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "pickup"))
        )
        pickup_input.clear()
        pickup_input.send_keys(location)
        
        # Dropdown
        print(f"   ⏳ Aguardando dropdown...")
        time.sleep(3)
        
        # Clicar dropdown
        clicked = False
        try:
            dropdown_item = WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "#recogida_lista li:first-child a"))
            )
            dropdown_item.click()
            clicked = True
            print(f"   ✅ Dropdown clicado!")
        except:
            result = driver.execute_script("""
                const items = document.querySelectorAll('#recogida_lista li');
                for (let item of items) {
                    if (item.offsetParent !== null) {
                        item.click();
                        return true;
                    }
                }
                return false;
            """)
            if result:
                clicked = True
                print(f"   ✅ Dropdown clicado (JS)!")
        
        if not clicked:
            print(f"   ❌ Falhou ao clicar dropdown")
            driver.quit()
            results.append({
                'device': device['name'],
                'success': False,
                'error': 'Dropdown click failed'
            })
            continue
        
        time.sleep(1)
        
        # Preencher datas e horas
        print(f"   📝 Preenchendo formulário...")
        result = driver.execute_script("""
            function fill(sel, val) {
                const el = document.querySelector(sel);
                if (el) { 
                    el.value = val; 
                    el.dispatchEvent(new Event('change', {bubbles: true}));
                    return true;
                }
                return false;
            }
            
            const r1 = fill('input[id="fechaRecogida"]', arguments[0]);
            const r2 = fill('input[id="fechaDevolucion"]', arguments[1]);
            
            const h1 = document.querySelector('select[id="fechaRecogidaSelHour"]');
            let h1_ok = false;
            if (h1) { h1.value = '15:00'; h1.dispatchEvent(new Event('change')); h1_ok = true; }
            
            const h2 = document.querySelector('select[id="fechaDevolucionSelHour"]');
            let h2_ok = false;
            if (h2) { h2.value = '15:00'; h2.dispatchEvent(new Event('change')); h2_ok = true; }
            
            return r1 && r2 && h1_ok && h2_ok;
        """, start_date.strftime("%d/%m/%Y"), end_date.strftime("%d/%m/%Y"))
        
        if not result:
            print(f"   ⚠️  Formulário incompleto")
        
        # Submit
        print(f"   🚀 Submetendo...")
        driver.execute_script("window.scrollBy(0, 300);")
        time.sleep(0.5)
        driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(0.5)
        driver.execute_script("document.querySelector('form').submit();")
        
        # Aguardar
        time.sleep(5)
        
        final_url = driver.current_url
        elapsed = time.time() - start_time
        
        # Verificar sucesso
        success = '/do/list/' in final_url and 's=' in final_url and 'b=' in final_url
        
        if success:
            print(f"   ✅ SUCESSO! ({elapsed:.1f}s)")
            print(f"   📍 URL: {final_url[:80]}...")
        else:
            print(f"   ❌ FALHOU ({elapsed:.1f}s)")
            print(f"   📍 URL: {final_url[:80]}...")
        
        results.append({
            'device': device['name'],
            'success': success,
            'url': final_url,
            'time': elapsed
        })
        
        driver.quit()
        
        # Pausa entre testes
        if idx < len(mobile_devices):
            print(f"\n   ⏸️  Pausa de 3 segundos antes do próximo teste...")
            time.sleep(3)
        
    except Exception as e:
        print(f"   ❌ ERRO: {e}")
        results.append({
            'device': device['name'],
            'success': False,
            'error': str(e)
        })
        driver.quit()

# RESUMO FINAL
print("\n" + "═" * 80)
print("📊 RESUMO FINAL - TODOS OS DISPOSITIVOS")
print("═" * 80)

success_count = sum(1 for r in results if r.get('success'))
total_count = len(results)

for i, result in enumerate(results, 1):
    status = "✅ SUCESSO" if result.get('success') else "❌ FALHOU"
    device = result['device']
    time_taken = f"{result.get('time', 0):.1f}s" if 'time' in result else "N/A"
    
    print(f"\n{i}. {device}")
    print(f"   Status: {status}")
    print(f"   Tempo: {time_taken}")
    if 'url' in result:
        has_params = 's=' in result['url'] and 'b=' in result['url']
        print(f"   Parâmetros s= e b=: {'✅' if has_params else '❌'}")

print("\n" + "═" * 80)
print(f"🎯 TAXA DE SUCESSO: {success_count}/{total_count} ({success_count/total_count*100:.0f}%)")
print("═" * 80)

if success_count == total_count:
    print("\n🎉 PERFEITO! Todos os dispositivos funcionaram!")
elif success_count > 0:
    print(f"\n⚠️  {total_count - success_count} dispositivo(s) falharam")
else:
    print("\n❌ Todos os dispositivos falharam")

print("\n✅ Teste completo!")
