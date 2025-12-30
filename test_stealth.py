#!/usr/bin/env python3
"""Teste com selenium-stealth para bypass de detecção"""

import time
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium_stealth import stealth

def test_carjet():
    print("🚀 Teste com Safari iPhone (emulação)...")
    
    # User agent de Safari no iPhone
    iphone_ua = "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"
    
    options = Options()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument(f"--user-agent={iphone_ua}")
    options.add_argument("--window-size=390,844")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    
    # Emulação mobile iPhone
    mobile_emulation = {
        "deviceMetrics": {"width": 390, "height": 844, "pixelRatio": 3.0},
        "userAgent": iphone_ua
    }
    options.add_experimental_option("mobileEmulation", mobile_emulation)
    
    driver = None
    try:
        driver = webdriver.Chrome(options=options)
        
        # Aplicar stealth com config de iPhone/Safari
        stealth(driver,
            languages=["pt-PT", "pt", "en"],
            vendor="Apple Computer, Inc.",
            platform="iPhone",
            webgl_vendor="Apple Inc.",
            renderer="Apple GPU",
            fix_hairline=True,
        )
        
        driver.set_page_load_timeout(30)
        
        # Abrir CarJet
        url = "https://www.carjet.com/aluguel-carros/index.htm"
        print(f"📍 Abrindo: {url}")
        driver.get(url)
        
        print(f"✅ Página: {driver.title}")
        print(f"🔗 URL: {driver.current_url}")
        
        # Rejeitar cookies - IGUAL AO MAIN.PY
        for i in range(2):
            time.sleep(0.5)
            print(f"🍪 Rejeitando cookies ({i+1})...")
            result = driver.execute_script("""
                // Procurar e clicar no botão de REJEITAR cookies
                const buttons = document.querySelectorAll('button, a, [role="button"]');
                let found = false;
                for (let btn of buttons) {
                    const text = btn.textContent.toLowerCase().trim();
                    // Procurar por "rejeitar", "recusar", "reject", etc.
                    if (text.includes('rejeitar') || text.includes('recusar') || 
                        text.includes('reject') || text.includes('rechazar') ||
                        text.includes('não aceitar') || text.includes('decline')) {
                        btn.click();
                        found = true;
                        return 'clicked: ' + text.substring(0, 30);
                    }
                }
                // Se não encontrou botão de rejeitar, tentar fechar/remover o banner
                if (!found) {
                    document.querySelectorAll('[id*=cookie], [class*=cookie], [id*=consent], [class*=consent]').forEach(el => {
                        el.remove();
                    });
                }
                document.body.style.overflow = 'auto';
                return found ? 'found' : 'removed_banner';
            """)
            print(f"   ✅ {result}")
            time.sleep(0.5)
        
        time.sleep(1)
        
        # Verificar se foi bloqueado
        if 'war=' in driver.current_url:
            print("❌ BLOQUEADO (WAR detectado)")
            return
        
        print("✅ Não bloqueado! Preenchendo formulário...")
        
        # Datas de teste - usar datas FUTURAS (Janeiro 2026)
        start_dt = datetime(2026, 1, 10, 10, 0)
        end_dt = datetime(2026, 1, 13, 10, 0)
        
        # PASSO 1: Preencher localização e clicar no dropdown
        print("📍 PASSO 1: Preenchendo localização...")
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        
        try:
            pickup_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "pickup"))
            )
            pickup_input.click()
            time.sleep(0.3)
            pickup_input.clear()
            pickup_input.send_keys("faro aero")
            print("   ✅ Local digitado: Faro")
            
            # Aguardar dropdown aparecer
            time.sleep(2)
            
            # Debug: ver se dropdown existe
            dropdown_info = driver.execute_script("""
                const list = document.querySelector('#recogida_lista');
                if (!list) return 'lista não existe';
                const items = list.querySelectorAll('li');
                return 'items: ' + items.length + ' - visible: ' + (list.offsetParent !== null);
            """)
            print(f"   📋 Dropdown: {dropdown_info}")
            
            # Clicar no item do dropdown
            print("📍 PASSO 2: Clicando no dropdown...")
            clicked = driver.execute_script("""
                const list = document.querySelector('#recogida_lista');
                if (!list) return 'no list';
                const items = list.querySelectorAll('li a');
                for (const a of items) {
                    if (a.textContent.includes('Faro')) {
                        a.click();
                        return 'clicked: ' + a.textContent.substring(0, 40);
                    }
                }
                // Tentar clicar em qualquer li
                const lis = list.querySelectorAll('li');
                if (lis.length > 0) {
                    lis[0].click();
                    return 'clicked li: ' + lis[0].textContent.substring(0, 40);
                }
                return 'nothing to click';
            """)
            print(f"   ✅ {clicked}")
            
            # IMPORTANTE: Clicar na página para confirmar o local
            time.sleep(0.5)
            print("📍 Clicando na página para confirmar local...")
            # Clicar num elemento específico da página (título)
            driver.find_element(By.CSS_SELECTOR, "h1, h2, .title, header").click()
            print("   ✅ Clicado na página")
            
        except Exception as e:
            print(f"   ⚠️ Erro localização: {e}")
        
        time.sleep(1)
        
        # PASSO 3: Preencher datas via campos hidden (versão mobile)
        print(f"📅 PASSO 3: Preenchendo datas: {start_dt.strftime('%d/%m/%Y')} - {end_dt.strftime('%d/%m/%Y')}")
        
        # Formato dd/mm/yyyy para campos hidden
        fecha_recogida = start_dt.strftime("%d/%m/%Y")
        fecha_devolucion = end_dt.strftime("%d/%m/%Y")
        
        result = driver.execute_script("""
            const fechaRecogida = arguments[0];
            const fechaDevolucion = arguments[1];
            
            let filled = {};
            
            // Campos hidden de data (formato dd/mm/yyyy)
            const fechaRec = document.querySelector('#fechaRecogida');
            const fechaDev = document.querySelector('#fechaDevolucion');
            
            if (fechaRec) { 
                fechaRec.value = fechaRecogida; 
                filled.fechaRec = fechaRec.value; 
            }
            if (fechaDev) { 
                fechaDev.value = fechaDevolucion; 
                filled.fechaDev = fechaDev.value; 
            }
            
            // Horas (selects)
            const h1 = document.querySelector('#fechaRecogidaSelHour');
            if (h1) { 
                h1.value = '10:00'; 
                h1.dispatchEvent(new Event('change', {bubbles: true})); 
                filled.h1 = h1.value; 
            }
            
            const h2 = document.querySelector('#fechaDevolucionSelHour');
            if (h2) { 
                h2.value = '10:00'; 
                h2.dispatchEvent(new Event('change', {bubbles: true})); 
                filled.h2 = h2.value; 
            }
            
            return filled;
        """, fecha_recogida, fecha_devolucion)
        print(f"   ✅ Datas: {result}")
        
        time.sleep(1)
        
        # Submit via botão (versão mobile usa searchCars())
        print("🔍 Submetendo...")
        driver.execute_script("""
            // Tentar clicar no botão Pesquisar
            const btn = document.querySelector('#btnBuscar');
            if (btn) { 
                btn.click(); 
            } else {
                // Fallback: submeter formulário
                const form = document.querySelector('#frm_search_cars') || document.querySelector('form');
                if (form) form.submit();
            }
        """)
        
        # Aguardar resultados
        print("⏳ Aguardando resultados...")
        for i in range(15):
            time.sleep(2)
            url = driver.current_url
            print(f"   {i*2}s: {url[:60]}...")
            if '/do/list/' in url and 'war=' not in url:
                print("✅ Página de resultados!")
                break
            if 'war=' in url:
                print("❌ BLOQUEADO após submit")
                break
        
        print(f"\n🔗 URL final: {driver.current_url}")
        print("\n⏳ Pressione Enter para fechar...")
        input()
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    test_carjet()
