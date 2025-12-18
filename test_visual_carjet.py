#!/usr/bin/env python3
"""
Teste visual do CarJet MOBILE - URL direta com parâmetros
Datas: 15 abril - 22 abril 2025, Aeroporto de Faro
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
from urllib.parse import urlencode

def test_carjet_visual():
    print("=" * 60)
    print("TESTE VISUAL CARJET - AEROPORTO DE FARO")
    print("Datas: 15/04/2025 - 22/04/2025")
    print("Método: URL direta com parâmetros + iPhone emulation")
    print("=" * 60)
    
    # Configurar Chrome COM interface gráfica - MODO MOBILE
    chrome_options = Options()
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    # Emulação de dispositivo móvel (iPhone 13 Pro)
    mobile_emulation = {
        "deviceMetrics": {"width": 390, "height": 844, "pixelRatio": 3.0},
        "userAgent": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1"
    }
    chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
    
    driver = None
    try:
        print("\n[1] Iniciando Chrome (iPhone mode)...")
        driver = webdriver.Chrome(options=chrome_options)
        driver.set_page_load_timeout(60)
        
        # Remover flag de automação
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        # Primeiro visitar homepage para obter cookies
        print("[2] Visitando homepage para cookies...")
        driver.get("https://www.carjet.com/aluguel-carros/index.htm")
        time.sleep(2)
        
        # Rejeitar cookies se aparecer
        print("[3] Verificando cookies...")
        try:
            driver.execute_script("""
                const buttons = document.querySelectorAll('button, a, [role="button"]');
                for (let btn of buttons) {
                    const text = btn.textContent.toLowerCase().trim();
                    if (text.includes('rejeitar') || text.includes('recusar') || 
                        text.includes('reject') || text.includes('decline')) {
                        btn.click();
                        console.log('Cookies rejeitados');
                        break;
                    }
                }
                document.querySelectorAll('[id*=cookie], [class*=cookie], [id*=consent]').forEach(el => el.remove());
            """)
            print("   ✓ Cookies tratados")
        except Exception as e:
            print(f"   ⚠ Cookies: {e}")
        
        time.sleep(1)
        
        # PASSO 1: Preencher local - LETRA POR LETRA para acionar autocomplete
        print("[4] Preenchendo local: Faro Airport (letra por letra)...")
        pickup_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "pickup"))
        )
        pickup_input.click()
        time.sleep(0.3)
        pickup_input.clear()
        time.sleep(0.3)
        
        # Digitar letra por letra
        location = "Faro Airport"
        for char in location:
            pickup_input.send_keys(char)
            time.sleep(0.05)
        print(f"   ✓ Local digitado: {location}")
        
        # PASSO 2: ESPERAR e CLICAR no dropdown (OBRIGATÓRIO)
        print("[5] Aguardando dropdown aparecer...")
        
        dropdown_clicked = False
        try:
            # Usar WebDriverWait para esperar pelo dropdown
            dropdown_item = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#recogida_lista li a"))
            )
            print(f"   ✓ Dropdown apareceu: {dropdown_item.text[:50] if dropdown_item.text else 'sem texto'}")
            dropdown_item.click()
            dropdown_clicked = True
            print("   ✅ Dropdown clicado com WebDriverWait!")
        except Exception as e:
            print(f"   ⚠️ WebDriverWait falhou: {e}")
            
            # Fallback: tentar via JavaScript
            for attempt in range(5):
                time.sleep(1)
                try:
                    js_result = driver.execute_script("""
                        const selectors = ['#recogida_lista li a', '#recogida_lista li', '.ui-autocomplete li a'];
                        for (const sel of selectors) {
                            const items = document.querySelectorAll(sel);
                            if (items.length > 0) {
                                items[0].click();
                                return {success: true, selector: sel, text: items[0].textContent?.substring(0, 50)};
                            }
                        }
                        const lista = document.querySelector('#recogida_lista');
                        return {success: false, html: lista ? lista.innerHTML.substring(0, 200) : 'lista não encontrada'};
                    """)
                    if js_result.get('success'):
                        print(f"   ✅ Dropdown clicado via JS: {js_result}")
                        dropdown_clicked = True
                        break
                    else:
                        print(f"   Tentativa {attempt+1}/5: {js_result}")
                except Exception as e2:
                    print(f"   Erro tentativa {attempt+1}: {e2}")
        
        if not dropdown_clicked:
            print("   ❌ ERRO: Dropdown não clicado - abortando!")
            raise Exception("Dropdown não clicado")
        
        time.sleep(1)
        
        # PASSO 3: Preencher datas - formato DD/MM/YYYY
        print("[6] Preenchendo datas: 15/04/2025 - 22/04/2025...")
        result = driver.execute_script("""
            function fill(sel, val) {
                const el = document.querySelector(sel);
                if (el) { 
                    el.focus();
                    el.value = val; 
                    el.dispatchEvent(new Event('input', {bubbles: true}));
                    el.dispatchEvent(new Event('change', {bubbles: true}));
                    el.dispatchEvent(new Event('blur', {bubbles: true}));
                    return true;
                }
                return false;
            }
            
            // Tentar diferentes seletores para as datas
            let r1 = fill('#fechaRecogida', arguments[0]) || 
                     fill('input[name="fechaRecogida"]', arguments[0]);
            let r2 = fill('#fechaDevolucion', arguments[1]) || 
                     fill('#fechaEntrega', arguments[1]) ||
                     fill('input[name="fechaDevolucion"]', arguments[1]) ||
                     fill('input[name="fechaEntrega"]', arguments[1]);
            
            // Preencher horas
            const hourSelectors = [
                '#fechaRecogidaSelHour', 'select[name="fechaRecogidaSelHour"]',
                '#fechaDevolucionSelHour', '#fechaEntregaSelHour', 
                'select[name="fechaDevolucionSelHour"]', 'select[name="fechaEntregaSelHour"]'
            ];
            
            let h1 = document.querySelector('#fechaRecogidaSelHour') || 
                     document.querySelector('select[name="fechaRecogidaSelHour"]');
            let h2 = document.querySelector('#fechaDevolucionSelHour') || 
                     document.querySelector('#fechaEntregaSelHour') ||
                     document.querySelector('select[name="fechaDevolucionSelHour"]') ||
                     document.querySelector('select[name="fechaEntregaSelHour"]');
            
            if (h1) { h1.value = '15:00'; h1.dispatchEvent(new Event('change', {bubbles: true})); }
            if (h2) { h2.value = '15:00'; h2.dispatchEvent(new Event('change', {bubbles: true})); }
            
            return {
                fechaRecogida: r1,
                fechaDevolucion: r2,
                hora1: h1 ? h1.value : 'not found',
                hora2: h2 ? h2.value : 'not found'
            };
        """, "15/04/2025", "22/04/2025")
        print(f"   ✓ Resultado: {result}")
        
        time.sleep(1)
        
        # PASSO 4: Clicar no botão de pesquisa (não form.submit)
        print("[7] Procurando botão de pesquisa...")
        driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(0.5)
        
        submit_result = driver.execute_script("""
            // Tentar clicar no botão de submit
            const buttons = document.querySelectorAll('button[type="submit"], input[type="submit"], .btn-search, .search-btn, button.btn');
            for (let btn of buttons) {
                const text = btn.textContent?.toLowerCase() || btn.value?.toLowerCase() || '';
                if (text.includes('buscar') || text.includes('pesquisar') || text.includes('search') || 
                    text.includes('procurar') || text.includes('ver') || btn.type === 'submit') {
                    btn.click();
                    return 'clicked button: ' + (btn.textContent || btn.value || btn.className);
                }
            }
            // Fallback: submit do form
            let form = document.querySelector('form[name="menu_tarifas"]') || 
                       document.querySelector('form#booking_form') ||
                       document.querySelector('form');
            if (form) {
                form.submit();
                return 'form.submit()';
            }
            return 'NO_BUTTON_OR_FORM';
        """)
        print(f"   ✓ Submit: {submit_result}")
        
        # Aguardar resultados
        print("[8] Aguardando página de resultados...")
        max_wait = 30
        waited = 0
        while waited < max_wait:
            current_url = driver.current_url
            print(f"   URL ({waited}s): {current_url[:80]}...")
            
            if '/do/list/' in current_url and 's=' in current_url:
                print(f"\n   ✅ Página de resultados carregada!")
                break
            elif 'war=' in current_url:
                print(f"\n   ⚠️ Erro detectado na URL: war=...")
                break
            
            time.sleep(2)
            waited += 2
        
        # Aguardar mais para carregar carros
        print("[9] Aguardando carregamento de carros...")
        time.sleep(5)
        
        # Verificar resultados
        final_url = driver.current_url
        print(f"\n{'=' * 60}")
        print(f"URL FINAL: {final_url}")
        print(f"{'=' * 60}")
        
        if 'war=' in final_url:
            import urllib.parse
            params = urllib.parse.parse_qs(urllib.parse.urlparse(final_url).query)
            war_code = params.get('war', ['?'])[0]
            print(f"\n❌ ERRO: war={war_code}")
            print("   Possíveis causas:")
            print("   - war=28: Nenhum veículo disponível para estas datas")
            print("   - war=29: Local não reconhecido")
            print("   - war=30: Data inválida")
        else:
            # Contar carros
            try:
                car_count = driver.execute_script("""
                    const cards = document.querySelectorAll('.car-card, .vehicle-card, [class*="car"], [class*="vehicle"]');
                    return cards.length;
                """)
                print(f"\n✅ Carros encontrados: {car_count}")
            except:
                print("\n⚠️ Não foi possível contar carros")
        
        print("\n" + "=" * 60)
        print("Janela do browser vai permanecer aberta para inspecção.")
        print("Prima ENTER para fechar...")
        print("=" * 60)
        input()
        
    except Exception as e:
        print(f"\n❌ ERRO: {e}")
        import traceback
        traceback.print_exc()
        
        if driver:
            print("\nJanela do browser vai permanecer aberta para inspecção.")
            print("Prima ENTER para fechar...")
            input()
    
    finally:
        if driver:
            driver.quit()
            print("\nBrowser fechado.")

if __name__ == "__main__":
    test_carjet_visual()
