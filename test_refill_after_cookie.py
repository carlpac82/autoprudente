#!/usr/bin/env python3
"""
Teste que REPREENCHE tudo após cookie limpar o formulário
Simula: preencher → cookie limpa → detecta → preenche TUDO novamente
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
print("TESTE - REPREENCHER APÓS COOKIE LIMPAR FORMULÁRIO", flush=True)
print("=" * 80, flush=True)

start_dt = datetime.now() + timedelta(days=7)
end_dt = start_dt + timedelta(days=5)

chrome_options = Options()
chrome_options.add_argument('--start-maximized')

print("\n🚀 Iniciando Chrome...", flush=True)
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

def accept_cookies():
    result = driver.execute_script("""
        const buttons = document.querySelectorAll('button');
        let found = false;
        for (let btn of buttons) {
            if (btn.textContent.toLowerCase().includes('aceitar todos')) {
                btn.click();
                found = true;
                break;
            }
        }
        document.querySelectorAll('[id*=cookie], [class*=cookie]').forEach(el => el.remove());
        return found;
    """)
    return result

try:
    print("\n1️⃣  Abrindo página...", flush=True)
    driver.get("https://www.carjet.com/aluguel-carros/index.htm")
    time.sleep(2)
    if accept_cookies():
        print("   ✅ Cookie inicial aceite", flush=True)
    time.sleep(1)
    
    print("\n2️⃣  Preenchendo local...", flush=True)
    pickup = driver.find_element(By.ID, "pickup")
    pickup.clear()
    pickup.send_keys("Albufeira Cidade")
    time.sleep(2)
    driver.execute_script("document.querySelector('#recogida_lista li[data-id=\"Albufeira Cidade\"]').click();")
    time.sleep(1)
    if accept_cookies():
        print("   ✅ Cookie após dropdown aceite", flush=True)
    
    print("\n3️⃣  Preenchendo formulário COM RETRY...", flush=True)
    form_filled = False
    
    for attempt in range(3):
        if form_filled:
            break
        
        print(f"\n   📝 Tentativa {attempt + 1}/3", flush=True)
        
        # Preencher TUDO
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
            
            // Preencher LOCAL (pode ter sido limpo)
            const pickup = fill('input[id="pickup"]', arguments[0]);
            
            // Preencher datas
            const r1 = fill('input[id="fechaRecogida"]', arguments[1]);
            const r2 = fill('input[id="fechaDevolucion"]', arguments[2]);
            
            // Preencher horas
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
        """, 
        "Albufeira Cidade",
        start_dt.strftime("%d/%m/%Y"),
        end_dt.strftime("%d/%m/%Y")
        )
        
        print(f"   Resultado: {result}", flush=True)
        
        if result.get('allFilled'):
            form_filled = True
            print(f"   ✅ TUDO PREENCHIDO!", flush=True)
        else:
            print(f"   ⚠️  Incompleto", flush=True)
            # Verificar se cookie limpou
            if attempt < 2:
                print(f"   🍪 Verificando se cookie limpou formulário...", flush=True)
                if accept_cookies():
                    print(f"   ✅ Cookie aceite! Preenchendo TUDO novamente...", flush=True)
                    time.sleep(1)
                else:
                    print(f"   ℹ️  Sem cookies, aguardando...", flush=True)
                    time.sleep(0.5)
    
    if not form_filled:
        print(f"\n   ❌ Não preencheu após 3 tentativas", flush=True)
    
    # Verificar valores finais
    print("\n🔍 Verificando valores finais...", flush=True)
    values = driver.execute_script("""
        return {
            pickup: document.querySelector('input[id="pickup"]')?.value || 'VAZIO',
            fechaRecogida: document.querySelector('input[id="fechaRecogida"]')?.value || 'VAZIO',
            fechaDevolucion: document.querySelector('input[id="fechaDevolucion"]')?.value || 'VAZIO',
            horaRecogida: document.querySelector('select[id="fechaRecogidaSelHour"]')?.value || 'VAZIO',
            horaDevolucion: document.querySelector('select[id="fechaDevolucionSelHour"]')?.value || 'VAZIO'
        };
    """)
    
    all_ok = True
    for key, val in values.items():
        if val == 'VAZIO':
            print(f"   ❌ {key}: VAZIO", flush=True)
            all_ok = False
        else:
            print(f"   ✅ {key}: {val}", flush=True)
    
    if not all_ok:
        print(f"\n   ⚠️  Alguns campos vazios! NÃO submeter.", flush=True)
    else:
        accept_cookies()
        
        print("\n4️⃣  Submetendo formulário...", flush=True)
        driver.execute_script("document.querySelector('form').submit();")
        time.sleep(5)
        accept_cookies()
        time.sleep(2)
        
        url = driver.current_url
        print(f"\n📄 URL final: {url}", flush=True)
        
        if "/do/list/" in url:
            print("\n🎉 SUCESSO! Chegou nos resultados!", flush=True)
            articles = driver.find_elements(By.CSS_SELECTOR, "section.newcarlist article")
            print(f"🚗 {len(articles)} carros encontrados", flush=True)
        elif "war=" in url:
            war = url.split("war=")[1].split("&")[0]
            print(f"\n❌ ERRO: war={war}", flush=True)
        else:
            print(f"\n⚠️  URL inesperada", flush=True)
    
    print("\n⏱️  Chrome aberto 90 segundos", flush=True)
    time.sleep(90)
    
except Exception as e:
    print(f"\n❌ ERRO: {e}", flush=True)
    import traceback
    traceback.print_exc()
    time.sleep(30)
finally:
    driver.quit()
    print("\n👋 Fechado", flush=True)
