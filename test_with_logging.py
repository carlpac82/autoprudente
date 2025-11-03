#!/usr/bin/env python3
"""
Teste com LOGGING COMPLETO
Grava tudo num ficheiro para análise
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

# Criar ficheiro de log
log_file = f"/Users/filipepacheco/CascadeProjects/RentalPriceTrackerPerDay/test_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

def log(msg):
    """Escreve no terminal e no ficheiro"""
    timestamp = datetime.now().strftime('%H:%M:%S.%f')[:-3]
    full_msg = f"[{timestamp}] {msg}"
    print(full_msg, flush=True)
    with open(log_file, 'a') as f:
        f.write(full_msg + '\n')

log("=" * 80)
log("TESTE COM LOGGING COMPLETO")
log("=" * 80)
log(f"Log file: {log_file}")

start_dt = datetime.now() + timedelta(days=7)
end_dt = start_dt + timedelta(days=5)

chrome_options = Options()
chrome_options.add_argument('--start-maximized')

log("\n🚀 Iniciando Chrome...")
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

def accept_cookies(step):
    """Aceita cookies e loga"""
    log(f"🍪 [{step}] Verificando cookies...")
    try:
        result = driver.execute_script("""
            const buttons = document.querySelectorAll('button');
            let found = false;
            let buttonText = '';
            for (let btn of buttons) {
                const text = btn.textContent.toLowerCase().trim();
                if (text.includes('aceitar todos') || text.includes('aceitar tudo')) {
                    buttonText = btn.textContent;
                    btn.click();
                    found = true;
                    break;
                }
            }
            document.querySelectorAll('[id*=cookie], [class*=cookie]').forEach(el => el.remove());
            return {found: found, buttonText: buttonText};
        """)
        if result['found']:
            log(f"   ✅ [{step}] Cookie aceite: '{result['buttonText']}'")
            return True
        else:
            log(f"   ℹ️  [{step}] Sem cookies")
            return False
    except Exception as e:
        log(f"   ❌ [{step}] Erro: {e}")
        return False

def check_form_values():
    """Verifica valores atuais do formulário"""
    log("🔍 Verificando valores do formulário...")
    try:
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
            log(f"   {status} {key}: {val}")
        return values
    except Exception as e:
        log(f"   ❌ Erro ao verificar: {e}")
        return None

def fill_form(location, date_rec, date_dev):
    """Preenche formulário completo"""
    log(f"📝 Preenchendo formulário...")
    log(f"   Local: {location}")
    log(f"   Data recolha: {date_rec}")
    log(f"   Data devolução: {date_dev}")
    
    try:
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
            
            return {
                pickup: pickup,
                fechaRecogida: r1,
                fechaDevolucion: r2,
                horaRecogida: !!h1,
                horaDevolucion: !!h2,
                allFilled: pickup && r1 && r2 && h1 && h2
            };
        """, location, date_rec, date_dev)
        
        log(f"   Resultado: {result}")
        return result.get('allFilled', False)
    except Exception as e:
        log(f"   ❌ Erro ao preencher: {e}")
        return False

try:
    log("\n" + "="*80)
    log("ESTADO 1: Abrir página")
    log("="*80)
    driver.get("https://www.carjet.com/aluguel-carros/index.htm")
    time.sleep(2)
    accept_cookies("INICIAL")
    time.sleep(1)
    
    log("\n" + "="*80)
    log("ESTADO 2: Preencher local")
    log("="*80)
    pickup = driver.find_element(By.ID, "pickup")
    pickup.clear()
    pickup.send_keys("Albufeira Cidade")
    log("   Digitado: Albufeira Cidade")
    time.sleep(2)
    
    log("\n" + "="*80)
    log("ESTADO 3: Clicar dropdown")
    log("="*80)
    driver.execute_script("document.querySelector('#recogida_lista li[data-id=\"Albufeira Cidade\"]').click();")
    log("   ✅ Dropdown clicado")
    time.sleep(1)
    
    # IMPORTANTE: Verificar cookies APÓS dropdown
    accept_cookies("APÓS DROPDOWN")
    time.sleep(1)
    
    log("\n" + "="*80)
    log("ESTADO 4: Preencher formulário COM RETRY")
    log("="*80)
    
    for attempt in range(3):
        log(f"\n--- Tentativa {attempt + 1}/3 ---")
        
        # Verificar estado atual
        check_form_values()
        
        # Preencher
        success = fill_form("Albufeira Cidade", start_dt.strftime("%d/%m/%Y"), end_dt.strftime("%d/%m/%Y"))
        
        if success:
            log("   ✅ Formulário preenchido!")
            break
        else:
            log("   ⚠️  Preenchimento incompleto")
            if attempt < 2:
                # Verificar se cookie apareceu e limpou
                if accept_cookies(f"RETRY {attempt + 1}"):
                    log("   🔄 Cookie limpou formulário! Tentando novamente...")
                    time.sleep(1)
                else:
                    time.sleep(0.5)
    
    log("\n" + "="*80)
    log("ESTADO 5: Verificação final antes de submeter")
    log("="*80)
    final_values = check_form_values()
    
    # Verificar se tudo está OK
    all_ok = all(v != 'VAZIO' for v in final_values.values()) if final_values else False
    
    if not all_ok:
        log("❌ CAMPOS VAZIOS! Não submeter.")
    else:
        accept_cookies("ANTES DE SUBMETER")
        
        log("\n" + "="*80)
        log("ESTADO 6: Submeter formulário")
        log("="*80)
        driver.execute_script("document.querySelector('form').submit();")
        log("   ✅ Formulário submetido")
        
        time.sleep(5)
        accept_cookies("APÓS SUBMETER")
        time.sleep(2)
        
        url = driver.current_url
        log(f"\n📄 URL final: {url}")
        
        if "/do/list/" in url:
            log("🎉 SUCESSO! Chegou nos resultados!")
        elif "war=" in url:
            war = url.split("war=")[1].split("&")[0]
            log(f"❌ ERRO: war={war}")
        else:
            log("⚠️  URL inesperada")
    
    log("\n" + "="*80)
    log("TESTE CONCLUÍDO")
    log(f"Log salvo em: {log_file}")
    log("="*80)
    
    log("\n⏱️  Chrome aberto 90 segundos")
    time.sleep(90)
    
except Exception as e:
    log(f"\n❌ ERRO GERAL: {e}")
    import traceback
    log(traceback.format_exc())
    time.sleep(30)
finally:
    driver.quit()
    log("\n👋 Chrome fechado")
    log(f"\n📄 Ver log completo em: {log_file}")
