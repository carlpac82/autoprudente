#!/usr/bin/env python3
"""
Teste completo do preenchimento do formulário Carjet Mobile
Seguindo os 8 passos documentados
"""
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import datetime, timedelta

# Configuração do Chrome
chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)

# Mobile emulation - iPhone 13
mobile_emulation = {
    "deviceMetrics": {"width": 390, "height": 844, "pixelRatio": 3.0},
    "userAgent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1"
}
chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)

# Caminho do Chrome no Mac
chrome_options.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

print("🚀 Iniciando Chrome...")
driver = webdriver.Chrome(options=chrome_options)

# Esconder webdriver
driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
    'source': '''
        Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined
        });
    '''
})

try:
    # Dados do teste
    location = "Faro Aeroporto"
    start_date = datetime.now() + timedelta(days=7)
    end_date = start_date + timedelta(days=3)
    pickup_time = "15:00"
    
    print(f"\n📋 DADOS DO TESTE:")
    print(f"   Local: {location}")
    print(f"   Recolha: {start_date.strftime('%d/%m/%Y')} às {pickup_time}")
    print(f"   Devolução: {end_date.strftime('%d/%m/%Y')} às {pickup_time}")
    print()
    
    # URL do Carjet em português
    url = "https://www.carjet.com/aluguel-carros/index.htm"
    print(f"📱 PASSO 0: Navegando para {url}")
    driver.get(url)
    time.sleep(2)
    
    # PASSO 1: ACEITAR/REJEITAR COOKIES
    print(f"\n✅ PASSO 1: Rejeitando cookies...")
    time.sleep(1)
    result = driver.execute_script("""
        const buttons = document.querySelectorAll('button, a, [role="button"]');
        let found = false;
        for (let btn of buttons) {
            const text = btn.textContent.toLowerCase().trim();
            if (text.includes('rejeitar') || text.includes('recusar') || 
                text.includes('reject') || text.includes('rechazar') ||
                text.includes('não aceitar') || text.includes('decline')) {
                btn.click();
                console.log('✓ Cookies rejeitados:', btn.textContent);
                found = true;
                break;
            }
        }
        if (!found) {
            document.querySelectorAll('[id*=cookie], [class*=cookie], [id*=didomi], [class*=didomi]').forEach(el => {
                el.remove();
            });
        }
        document.body.style.overflow = 'auto';
        return found;
    """)
    print(f"   {'✓ Cookies rejeitados' if result else '✓ Banner removido'}")
    time.sleep(1)
    
    # PASSO 2: ESCREVER O NOME DO LOCAL
    print(f"\n✅ PASSO 2: Escrevendo local '{location}'...")
    pickup_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "pickup"))
    )
    pickup_input.clear()
    pickup_input.send_keys(location)
    print(f"   ✓ Local digitado")
    
    # PASSO 3: AGUARDAR E CLICAR NO DROPDOWN
    print(f"\n✅ PASSO 3: Aguardando dropdown aparecer...")
    time.sleep(2)
    
    print(f"   Tentando clicar no item do dropdown...")
    clicked = False
    
    # Tentar múltiplos seletores
    selectors = [
        f"#recogida_lista li[data-id='{location}'] a",
        f"#recogida_lista li[data-id='{location}']",
        "#recogida_lista li:first-child a",
        "#recogida_lista li:first-child",
        "#recogida_lista li.history-list:first-child a",
        "#recogida_lista li.history-list:first-child",
    ]
    
    for selector in selectors:
        if clicked:
            break
        try:
            print(f"   Tentando: {selector}")
            dropdown_item = WebDriverWait(driver, 2).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
            )
            dropdown_item.click()
            clicked = True
            print(f"   ✓ Dropdown clicado via: {selector}")
            break
        except Exception as e:
            pass
    
    # Tentar via JavaScript se falhou
    if not clicked:
        print(f"   Tentando via JavaScript...")
        result = driver.execute_script("""
            // Tentar primeiro item visível
            const items = document.querySelectorAll('#recogida_lista li');
            console.log('Items encontrados:', items.length);
            
            for (let item of items) {
                if (item.offsetParent !== null) {  // Visível
                    console.log('Clicando em:', item.textContent);
                    item.click();
                    return true;
                }
            }
            
            // Tentar link dentro do primeiro item
            const link = document.querySelector('#recogida_lista li a');
            if (link) {
                console.log('Clicando em link:', link.textContent);
                link.click();
                return true;
            }
            
            return false;
        """)
        if result:
            clicked = True
            print(f"   ✓ Dropdown clicado via JavaScript")
        else:
            print(f"   ⚠️ JavaScript também falhou")
    
    if not clicked:
        print(f"   ❌ NÃO CONSEGUIU CLICAR NO DROPDOWN!")
        print(f"   Tentando ver o HTML do dropdown...")
        html = driver.execute_script("""
            const lista = document.querySelector('#recogida_lista');
            return lista ? lista.innerHTML : 'Dropdown não encontrado';
        """)
        print(f"   HTML: {html[:200]}...")
    else:
        print(f"   ✅ Dropdown clicado com sucesso!")
    
    time.sleep(1)
    
    # PASSOS 4-7: PREENCHER DATAS E HORAS VIA JAVASCRIPT
    print(f"\n✅ PASSOS 4-7: Preenchendo datas e horas...")
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
        
        // PASSO 4: Data de recolha
        const r1 = fill('input[id="fechaRecogida"]', arguments[0]);
        console.log('Data recolha:', r1);
        
        // PASSO 5: Data de devolução
        const r2 = fill('input[id="fechaDevolucion"]', arguments[1]);
        console.log('Data devolução:', r2);
        
        // PASSO 6: Hora de recolha
        const h1 = document.querySelector('select[id="fechaRecogidaSelHour"]');
        let h1_ok = false;
        if (h1) { 
            h1.value = arguments[2]; 
            h1.dispatchEvent(new Event('change', {bubbles: true}));
            h1_ok = true;
            console.log('Hora recolha:', h1.value);
        }
        
        // PASSO 7: Hora de devolução
        const h2 = document.querySelector('select[id="fechaDevolucionSelHour"]');
        let h2_ok = false;
        if (h2) { 
            h2.value = arguments[3]; 
            h2.dispatchEvent(new Event('change', {bubbles: true}));
            h2_ok = true;
            console.log('Hora devolução:', h2.value);
        }
        
        return {
            fechaRecogida: r1,
            fechaDevolucion: r2,
            horaRecogida: h1_ok,
            horaDevolucion: h2_ok,
            allFilled: r1 && r2 && h1_ok && h2_ok
        };
    """, start_date.strftime("%d/%m/%Y"), end_date.strftime("%d/%m/%Y"), pickup_time, pickup_time)
    
    print(f"   ✓ Data recolha: {result.get('fechaRecogida', False)}")
    print(f"   ✓ Data devolução: {result.get('fechaDevolucion', False)}")
    print(f"   ✓ Hora recolha: {result.get('horaRecogida', False)}")
    print(f"   ✓ Hora devolução: {result.get('horaDevolucion', False)}")
    
    if result.get('allFilled'):
        print(f"   ✅ Formulário completo preenchido!")
    else:
        print(f"   ⚠️ Preenchimento incompleto")
    
    time.sleep(1)
    
    # PASSO 8: CLICAR EM BUSCAR
    print(f"\n✅ PASSO 8: Submetendo formulário...")
    
    # Scroll simulation
    driver.execute_script("window.scrollBy(0, 300);")
    time.sleep(0.5)
    driver.execute_script("window.scrollTo(0, 0);")
    time.sleep(0.5)
    
    # Submit
    driver.execute_script("document.querySelector('form').submit();")
    print(f"   ✓ Formulário submetido")
    
    # Aguardar navegação
    print(f"\n⏳ Aguardando navegação para resultados...")
    time.sleep(5)
    
    final_url = driver.current_url
    print(f"\n📍 URL FINAL: {final_url}")
    
    if '/do/list/' in final_url:
        print(f"✅ SUCESSO! Navegou para página de resultados")
        if 's=' in final_url and 'b=' in final_url:
            print(f"✅ URL contém parâmetros s= e b=")
        else:
            print(f"⚠️ URL não contém s= ou b=")
    elif 'war=' in final_url:
        print(f"⚠️ AVISO: URL contém war= (sem disponibilidade)")
    else:
        print(f"⚠️ URL inesperada")
    
    print(f"\n⏳ Mantendo navegador aberto por 30 segundos para você ver...")
    print(f"🛑 Pressione Ctrl+C para fechar antes\n")
    time.sleep(30)
    
except KeyboardInterrupt:
    print("\n\n🛑 Interrompido pelo usuário")
except Exception as e:
    print(f"\n❌ ERRO: {e}")
    import traceback
    traceback.print_exc()
    print(f"\n⏳ Mantendo navegador aberto por 60 segundos para debug...")
    time.sleep(60)
finally:
    driver.quit()
    print("✅ Chrome fechado.")
