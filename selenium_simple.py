#!/usr/bin/env python3
"""
Função simplificada de Selenium - IGUAL AO TESTE
"""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import sys
from datetime import datetime

def scrape_carjet_simple(location, start_dt, end_dt):
    """
    Scraping simples usando código IDÊNTICO ao test_dates_specific.py
    
    Args:
        location: "Faro" ou "Albufeira"
        start_dt: datetime object
        end_dt: datetime object
    
    Returns:
        dict com 'ok', 'url', 'html' ou erro
    """
    
    # Mapear localização
    location_map = {
        'faro': 'Faro Aeroporto (FAO)',
        'albufeira': 'Albufeira Cidade'
    }
    carjet_location = location_map.get(location.lower(), 'Faro Aeroporto (FAO)')
    
    print(f"[SELENIUM_SIMPLE] Iniciando scraping...", file=sys.stderr, flush=True)
    print(f"[SELENIUM_SIMPLE] Local: {carjet_location}", file=sys.stderr, flush=True)
    print(f"[SELENIUM_SIMPLE] Datas: {start_dt.strftime('%d/%m/%Y')} - {end_dt.strftime('%d/%m/%Y')}", file=sys.stderr, flush=True)
    
    # Configurar Chrome
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    
    # Headless mode (invisível) - pode ser desativado com SHOW_BROWSER=1
    # No Render (produção), SEMPRE usa headless
    import os
    is_render = os.getenv('RENDER') or os.getenv('DATABASE_URL')
    show_browser = os.getenv('SHOW_BROWSER', '0') == '1' and not is_render
    
    if not show_browser:
        chrome_options.add_argument('--headless=new')  # Invisível
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        if is_render:
            print(f"[SELENIUM_SIMPLE] Modo headless (Render/Produção)", file=sys.stderr, flush=True)
        else:
            print(f"[SELENIUM_SIMPLE] Modo headless (invisível)", file=sys.stderr, flush=True)
    else:
        print(f"[SELENIUM_SIMPLE] Modo visível (debug local)", file=sys.stderr, flush=True)
    
    chrome_options.add_argument('user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1')
    
    mobile_emulation = {
        "deviceMetrics": {"width": 390, "height": 844, "pixelRatio": 3.0},
        "userAgent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1"
    }
    chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    
    driver = webdriver.Chrome(options=chrome_options)
    
    # Esconder webdriver
    driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
        'source': 'Object.defineProperty(navigator, "webdriver", { get: () => undefined });'
    })
    
    driver.set_page_load_timeout(20)
    
    def reject_cookies():
        try:
            result = driver.execute_script("""
                const buttons = document.querySelectorAll('button, a, [role="button"]');
                for (let btn of buttons) {
                    const text = btn.textContent.toLowerCase().trim();
                    if (text.includes('rejeitar') || text.includes('reject')) {
                        btn.click();
                        return true;
                    }
                }
                return false;
            """)
            return result
        except:
            return False
    
    try:
        # Navegar
        url = "https://www.carjet.com/aluguel-carros/index.htm"
        print(f"[SELENIUM_SIMPLE] Navegando para {url}", file=sys.stderr, flush=True)
        driver.get(url)
        
        # Cookies
        time.sleep(0.5)
        if reject_cookies():
            print("[SELENIUM_SIMPLE] ✅ Cookies rejeitados", file=sys.stderr, flush=True)
        time.sleep(0.5)
        
        # PASSO 1: Escrever local
        print(f"[SELENIUM_SIMPLE] PASSO 1: Escrevendo local...", file=sys.stderr, flush=True)
        pickup_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "pickup"))
        )
        pickup_input.clear()
        pickup_input.send_keys(carjet_location)
        print(f"[SELENIUM_SIMPLE] ✓ Local digitado", file=sys.stderr, flush=True)
        
        # PASSO 2: Dropdown
        print(f"[SELENIUM_SIMPLE] PASSO 2: Aguardando dropdown...", file=sys.stderr, flush=True)
        time.sleep(3)
        
        try:
            dropdown_item = WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "#recogida_lista li:first-child a"))
            )
            dropdown_item.click()
            print(f"[SELENIUM_SIMPLE] ✅ Dropdown clicado", file=sys.stderr, flush=True)
        except:
            driver.execute_script("""
                const items = document.querySelectorAll('#recogida_lista li');
                for (let item of items) {
                    if (item.offsetParent !== null) {
                        item.click();
                        return true;
                    }
                }
            """)
            print(f"[SELENIUM_SIMPLE] ✅ Dropdown clicado (JS)", file=sys.stderr, flush=True)
        
        time.sleep(1)
        
        # PASSO 3: Preencher datas e horas
        print(f"[SELENIUM_SIMPLE] PASSO 3: Preenchendo datas e horas...", file=sys.stderr, flush=True)
        
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
            
            // Preencher datas
            const r1 = fill('input[id="fechaRecogida"]', arguments[0]);
            const r2 = fill('input[id="fechaDevolucion"]', arguments[1]);
            
            // Preencher horas
            const h1 = document.querySelector('select[id="fechaRecogidaSelHour"]');
            let h1_ok = false;
            if (h1) { 
                h1.value = arguments[2]; 
                h1.dispatchEvent(new Event('change', {bubbles: true}));
                h1_ok = true;
            }
            
            const h2 = document.querySelector('select[id="fechaDevolucionSelHour"]');
            let h2_ok = false;
            if (h2) { 
                h2.value = arguments[3]; 
                h2.dispatchEvent(new Event('change', {bubbles: true}));
                h2_ok = true;
            }
            
            return {
                fechaRecogida: r1,
                fechaDevolucion: r2,
                horaRecogida: h1_ok,
                horaDevolucion: h2_ok,
                allFilled: r1 && r2 && h1_ok && h2_ok
            };
        """, start_dt.strftime("%d/%m/%Y"), end_dt.strftime("%d/%m/%Y"), 
             start_dt.strftime("%H:%M"), end_dt.strftime("%H:%M"))
        
        print(f"[SELENIUM_SIMPLE] ✓ Datas preenchidas: {result}", file=sys.stderr, flush=True)
        
        time.sleep(1)
        
        # PASSO 4: Submit
        print(f"[SELENIUM_SIMPLE] PASSO 4: Submetendo...", file=sys.stderr, flush=True)
        driver.execute_script("window.scrollBy(0, 300);")
        time.sleep(0.5)
        driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(0.5)
        driver.execute_script("document.querySelector('form').submit();")
        
        print(f"[SELENIUM_SIMPLE] Aguardando navegação...", file=sys.stderr, flush=True)
        time.sleep(5)
        
        # Aguardar redirect para /do/list/
        print(f"[SELENIUM_SIMPLE] Aguardando página de resultados...", file=sys.stderr, flush=True)
        max_wait = 40
        waited = 0
        while waited < max_wait:
            current_url = driver.current_url
            if '/do/list/' in current_url and 's=' in current_url and 'b=' in current_url:
                print(f"[SELENIUM_SIMPLE] ✅ Página carregada após {waited}s", file=sys.stderr, flush=True)
                break
            time.sleep(3)
            waited += 3
        
        # Aguardar conteúdo carregar
        time.sleep(5)
        
        final_url = driver.current_url
        print(f"[SELENIUM_SIMPLE] URL final: {final_url}", file=sys.stderr, flush=True)
        
        if '/do/list/' in final_url and 's=' in final_url and 'b=' in final_url:
            # Pegar HTML do driver
            html_content = driver.page_source
            driver.quit()
            
            print(f"[SELENIUM_SIMPLE] ✅ Sucesso! HTML: {len(html_content)} bytes", file=sys.stderr, flush=True)
            
            return {
                'ok': True,
                'url': final_url,
                'html': html_content
            }
        elif 'war=' in final_url:
            driver.quit()
            print(f"[SELENIUM_SIMPLE] ⚠️ URL com war= (sem disponibilidade)", file=sys.stderr, flush=True)
            return {
                'ok': False,
                'error': 'war_url',
                'url': final_url
            }
        else:
            driver.quit()
            print(f"[SELENIUM_SIMPLE] ❌ URL inesperada: {final_url}", file=sys.stderr, flush=True)
            return {
                'ok': False,
                'error': 'unexpected_url',
                'url': final_url
            }
            
    except Exception as e:
        try:
            driver.quit()
        except:
            pass
        print(f"[SELENIUM_SIMPLE] ❌ Erro: {e}", file=sys.stderr, flush=True)
        import traceback
        traceback.print_exc(file=sys.stderr)
        return {
            'ok': False,
            'error': str(e)
        }
