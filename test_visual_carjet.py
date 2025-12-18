#!/usr/bin/env python3
"""
Teste visual do CarJet - SELENIUM COM EMULAÇÃO MOBILE iPhone 13 Pro
Com RETRY automático após war=11
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import random

def reject_cookies(driver):
    """Rejeita cookies rapidamente"""
    try:
        # Tentar clicar no botão diretamente via JS (mais rápido)
        clicked = driver.execute_script("""
            const btns = document.querySelectorAll('button');
            for (let btn of btns) {
                if (btn.textContent.includes('Rejeitar todos')) {
                    btn.click();
                    return true;
                }
            }
            return false;
        """)
        if clicked:
            return True
        
        # Fallback: remover elementos
        driver.execute_script("""
            document.querySelectorAll('[id*=cookie], [class*=cookie], [id*=consent], [id*=didomi]').forEach(el => el.remove());
            document.body.style.overflow = 'auto';
        """)
        return True
    except:
        return False

def fill_form(driver, hora_recolha, hora_entrega):
    """Preenche o formulário completo"""
    # LOCAL
    print(f"    Preenchendo local: Faro...")
    pickup = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "pickup")))
    pickup.click()
    pickup.clear()
    pickup.send_keys("Faro")
    
    # DROPDOWN
    time.sleep(1.5)
    driver.execute_script("""
        const items = document.querySelectorAll('#recogida_lista li a');
        if (items.length > 0) items[0].click();
    """)
    time.sleep(0.5)
    
    # DATAS
    print(f"    Preenchendo datas: 15/04/2025 - 22/04/2025...")
    driver.execute_script("""
        const pickup = document.querySelector('#fechaRecogida');
        const dropoff = document.querySelector('#fechaDevolucion');
        if (pickup) { pickup.value = arguments[0]; pickup.dispatchEvent(new Event('change')); }
        if (dropoff) { dropoff.value = arguments[1]; dropoff.dispatchEvent(new Event('change')); }
    """, "15/04/2025", "22/04/2025")
    
    # HORAS
    print(f"    Preenchendo horas: recolha={hora_recolha}, entrega={hora_entrega}...")
    driver.execute_script("""
        const h1 = document.querySelector('#fechaRecogidaSelHour');
        const h2 = document.querySelector('#fechaDevolucionSelHour');
        if (h1) { h1.value = arguments[0]; h1.dispatchEvent(new Event('change')); }
        if (h2) { h2.value = arguments[1]; h2.dispatchEvent(new Event('change')); }
    """, hora_recolha, hora_entrega)
    
    time.sleep(0.5)

def submit_form(driver):
    """Submete o formulário"""
    driver.execute_script("""
        const btn = document.querySelector('#btnBuscar');
        if (btn) btn.click();
        else document.querySelector('form').submit();
    """)

def test_carjet_visual():
    print("=" * 60)
    print("TESTE VISUAL CARJET - iPhone 13 Pro + RETRY")
    print("=" * 60)
    
    chrome_options = Options()
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    mobile_emulation = {
        "deviceMetrics": {"width": 390, "height": 844, "pixelRatio": 3.0},
        "userAgent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1"
    }
    chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
    
    driver = None
    available_hours = ['15:00', '15:30', '16:00', '16:30', '17:00', '17:30']
    used_hours = []
    
    try:
        print("\n[1] Iniciando Chrome...")
        driver = webdriver.Chrome(options=chrome_options)
        driver.set_page_load_timeout(60)
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        print("[2] Abrindo CarJet...")
        driver.get("https://www.carjet.com/aluguel-carros/index.htm")
        time.sleep(2)
        
        # REJEITAR COOKIES RÁPIDO
        print("[3] Rejeitando cookies...")
        reject_cookies(driver)
        time.sleep(0.5)
        
        # ============ PASSO 1: LOCAL ============
        print("\n[4] PASSO 1: Preenchendo LOCAL...")
        pickup = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "pickup")))
        pickup.click()
        pickup.clear()
        pickup.send_keys("Faro")
        print("    ✓ Digitado: Faro")
        
        # ============ PASSO 2: DROPDOWN ============
        print("\n[5] PASSO 2: Aguardando DROPDOWN aparecer...")
        time.sleep(2)
        
        # Usar WebDriverWait para esperar e clicar no dropdown
        dropdown_clicked = False
        try:
            # Esperar pelo primeiro item do dropdown
            dropdown_item = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "#recogida_lista li:first-child a"))
            )
            print(f"    ✓ Dropdown apareceu: {dropdown_item.text[:40] if dropdown_item.text else 'item'}")
            dropdown_item.click()
            dropdown_clicked = True
            print("    ✅ Dropdown clicado!")
        except Exception as e:
            print(f"    ⚠️ WebDriverWait falhou: {e}")
            # Fallback: tentar via JavaScript
            for attempt in range(3):
                time.sleep(1)
                clicked = driver.execute_script("""
                    const items = document.querySelectorAll('#recogida_lista li a');
                    if (items.length > 0) { 
                        items[0].click(); 
                        return {success: true, text: items[0].textContent?.substring(0, 40)}; 
                    }
                    const lista = document.querySelector('#recogida_lista');
                    return {success: false, visible: lista?.style.display, html: lista?.innerHTML?.substring(0,100)};
                """)
                print(f"    Tentativa {attempt+1}: {clicked}")
                if clicked.get('success'):
                    dropdown_clicked = True
                    break
        
        if not dropdown_clicked:
            print("    ❌ ERRO: Dropdown não clicado!")
            input("    Prima ENTER para continuar...")
        
        time.sleep(1)
        
        # ============ PASSO 3: DATAS VIA DROPDOWNS DO MYBOOKING ============
        print("\n[6] PASSO 3: Preenchendo DATAS via dropdowns...")
        
        # O CarJet mobile usa dropdowns: fechaRecogidaMyBookingMonthYear e fechaRecogidaMyBookingDay
        date_result = driver.execute_script("""
            // Janeiro 2026 = 202601 (data FUTURA!)
            const monthYearValue = '202601';
            const dayPickup = '15';
            const dayDropoff = '22';
            
            // RECOLHA - Mês/Ano
            const monthSelect1 = document.querySelector('#fechaRecogidaMyBookingMonthYear');
            if (monthSelect1) {
                monthSelect1.value = monthYearValue;
                monthSelect1.dispatchEvent(new Event('change', {bubbles: true}));
            }
            
            // RECOLHA - Dia
            const daySelect1 = document.querySelector('#fechaRecogidaMyBookingDay');
            if (daySelect1) {
                daySelect1.value = dayPickup;
                daySelect1.dispatchEvent(new Event('change', {bubbles: true}));
            }
            
            // DEVOLUÇÃO - Mês/Ano
            const monthSelect2 = document.querySelector('#fechaDevolucionMyBookingMonthYear');
            if (monthSelect2) {
                monthSelect2.value = monthYearValue;
                monthSelect2.dispatchEvent(new Event('change', {bubbles: true}));
            }
            
            // DEVOLUÇÃO - Dia
            const daySelect2 = document.querySelector('#fechaDevolucionMyBookingDay');
            if (daySelect2) {
                daySelect2.value = dayDropoff;
                daySelect2.dispatchEvent(new Event('change', {bubbles: true}));
            }
            
            // Também preencher campos hidden
            const fechaRec = document.querySelector('#fechaRecogida');
            const fechaDev = document.querySelector('#fechaDevolucion');
            if (fechaRec) fechaRec.value = '15/01/2026';
            if (fechaDev) fechaDev.value = '22/01/2026';
            
            return {
                monthSelect1: monthSelect1?.value,
                daySelect1: daySelect1?.value,
                monthSelect2: monthSelect2?.value,
                daySelect2: daySelect2?.value,
                fechaRec: fechaRec?.value,
                fechaDev: fechaDev?.value
            };
        """)
        print(f"    Datas: {date_result}")
        time.sleep(1)
        
        # ============ PASSO 4: HORAS (ALEATÓRIAS entre 15:00 e 17:30) ============
        print("\n[7] PASSO 4: Preenchendo HORAS aleatórias...")
        
        import random
        # Horas disponíveis entre 15:00 e 17:30
        available_hours = ['15:00', '15:30', '16:00', '16:30', '17:00', '17:30']
        hora_recolha = random.choice(available_hours)
        hora_entrega = random.choice(available_hours)
        
        # Garantir que são diferentes
        while hora_entrega == hora_recolha:
            hora_entrega = random.choice(available_hours)
        
        print(f"    Hora recolha: {hora_recolha}, Hora entrega: {hora_entrega}")
        
        hour_result = driver.execute_script("""
            const h1 = document.querySelector('#fechaRecogidaSelHour');
            const h2 = document.querySelector('#fechaDevolucionSelHour') || document.querySelector('#fechaEntregaSelHour');
            
            if (h1) {
                h1.value = arguments[0];
                h1.dispatchEvent(new Event('change', {bubbles: true}));
            }
            if (h2) {
                h2.value = arguments[1];
                h2.dispatchEvent(new Event('change', {bubbles: true}));
            }
            
            return {hora1: h1?.value, hora2: h2?.value};
        """, hora_recolha, hora_entrega)
        print(f"    Horas definidas: {hour_result}")
        
        time.sleep(1)
        
        # ============ PASSO 5: VERIFICAR ANTES DO SUBMIT ============
        print("\n[8] Verificando formulário antes do submit...")
        form_values = driver.execute_script("""
            return {
                pickup: document.querySelector('#pickup')?.value,
                fechaRecogida: document.querySelector('#fechaRecogida')?.value,
                fechaDevolucion: (document.querySelector('#fechaDevolucion') || document.querySelector('#fechaEntrega'))?.value,
                horaRecogida: document.querySelector('#fechaRecogidaSelHour')?.value,
                horaDevolucion: (document.querySelector('#fechaDevolucionSelHour') || document.querySelector('#fechaEntregaSelHour'))?.value
            };
        """)
        print(f"    VALORES FINAIS: {form_values}")
        
        # Validar
        if not form_values.get('fechaRecogida') or not form_values.get('fechaDevolucion'):
            print("\n    ❌ ERRO: Datas não preenchidas!")
            print("    Aguardando para debug manual...")
            input("    Prima ENTER para continuar mesmo assim...")
        
        # ============ PASSO 6: SUBMIT ============
        print("\n[9] PASSO 5: Submetendo formulário...")
        driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(0.5)
        
        submit_result = driver.execute_script("""
            const form = document.querySelector('form[name="menu_tarifas"]') || document.querySelector('form');
            if (form) {
                form.submit();
                return 'form.submit()';
            }
            return 'NO_FORM';
        """)
        print(f"    Submit: {submit_result}")
        
        # Aguardar resultados
        print("[8] Aguardando página de resultados...")
        time.sleep(3)
        
        current_url = driver.current_url
        print(f"   URL: {current_url[:80]}...")
        
        # SE DEU WAR=11, FAZER RETRY COMPLETO
        if 'war=' in current_url:
            print("\n   ⚠️ war= detectado - fazendo RETRY COMPLETO...")
            
            # 1. Rejeitar cookies novamente
            print("   [RETRY 1/5] Rejeitando cookies...")
            reject_cookies(driver)
            time.sleep(0.5)
            
            # 2. Escolher HORAS DIFERENTES
            nova_hora_recolha = random.choice([h for h in available_hours if h != hora_recolha])
            nova_hora_entrega = random.choice([h for h in available_hours if h != hora_entrega and h != nova_hora_recolha])
            print(f"   [RETRY 2/5] Novas horas: recolha={nova_hora_recolha}, entrega={nova_hora_entrega}")
            
            # 3. Preencher LOCAL novamente
            print("   [RETRY 3/5] Preenchendo local...")
            pickup = driver.find_element(By.ID, "pickup")
            pickup.click()
            pickup.clear()
            pickup.send_keys("Faro")
            
            # 4. AGUARDAR E CLICAR NO DROPDOWN
            print("   [RETRY 4/5] Aguardando dropdown...")
            time.sleep(2)  # Aguardar dropdown aparecer
            
            dropdown_ok = False
            try:
                dropdown_item = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "#recogida_lista li:first-child a"))
                )
                dropdown_item.click()
                dropdown_ok = True
                print("   [RETRY] ✅ Dropdown clicado!")
            except:
                # Fallback JS
                driver.execute_script("""
                    const items = document.querySelectorAll('#recogida_lista li a');
                    if (items.length > 0) items[0].click();
                """)
                print("   [RETRY] Dropdown clicado via JS")
            
            time.sleep(1)
            
            # 5. Preencher DATAS (ABRIL 2025!) - hidden + spans visuais
            print("   [RETRY] Preenchendo datas (15/04/2025 - 22/04/2025)...")
            driver.execute_script("""
                // Hidden fields
                const pickup = document.querySelector('#fechaRecogida');
                const dropoff = document.querySelector('#fechaDevolucion');
                if (pickup) pickup.value = '15/04/2025';
                if (dropoff) dropoff.value = '22/04/2025';
                
                // Spans visuais recolha
                const d1 = document.querySelector('#fechaRecogida_Day');
                const m1 = document.querySelector('#fechaRecogida_MonthText');
                const y1 = document.querySelector('#fechaRecogida_Year');
                if (d1) d1.textContent = '15';
                if (m1) m1.textContent = 'Abr';
                if (y1) y1.textContent = '2025';
                
                // Spans visuais devolução
                const d2 = document.querySelector('#fechaDevolucion_Day');
                const m2 = document.querySelector('#fechaDevolucion_MonthText');
                const y2 = document.querySelector('#fechaDevolucion_Year');
                if (d2) d2.textContent = '22';
                if (m2) m2.textContent = 'Abr';
                if (y2) y2.textContent = '2025';
            """)
            
            # 6. Preencher HORAS NOVAS
            driver.execute_script("""
                const h1 = document.querySelector('#fechaRecogidaSelHour');
                const h2 = document.querySelector('#fechaDevolucionSelHour');
                if (h1) { h1.value = arguments[0]; h1.dispatchEvent(new Event('change')); }
                if (h2) { h2.value = arguments[1]; h2.dispatchEvent(new Event('change')); }
            """, nova_hora_recolha, nova_hora_entrega)
            time.sleep(0.5)
            
            # 7. Clicar em pesquisar
            print("   [RETRY 5/5] Clicando em pesquisar...")
            driver.execute_script("""
                const btn = document.querySelector('#btnBuscar');
                if (btn) btn.click();
            """)
            
            # Aguardar resultado do retry
            print("   [RETRY] Aguardando resultado...")
            time.sleep(5)
            current_url = driver.current_url
            print(f"   [RETRY] URL: {current_url[:80]}...")
        
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
