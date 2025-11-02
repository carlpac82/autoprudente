#!/usr/bin/env python3
"""
Script para observar ações do usuário no Chrome e registar tudo com timestamps
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

print("="*80)
print("🔍 OBSERVADOR DE AÇÕES DO USUÁRIO")
print("="*80)
print()
print("🚀 A ABRIR CHROME AUTOMATICAMENTE...")
print()
print("INSTRUÇÕES:")
print("1. O Chrome vai abrir AGORA")
print("2. Faz TUDO manualmente como se fosses um utilizador normal:")
print("   ✅ Aceita o 1º cookie")
print("   ✅ Preenche a localização (Albufeira Cidade)")
print("   ✅ Seleciona no dropdown")
print("   ✅ Preenche as datas")
print("   ✅ Aceita o 2º cookie (se aparecer)")
print("   ✅ Clica em Buscar")
print("3. Vou registar o TEMPO de cada ação")
print()
time.sleep(2)

# Configurar Chrome VISÍVEL
chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--disable-blink-features=AutomationControlled')
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)

# Iniciar driver
print("\n[SETUP] Iniciando Chrome...")
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=chrome_options
)

# Maximizar janela
driver.maximize_window()

# Timer
t0 = time.time()

def log(msg):
    elapsed = time.time() - t0
    print(f"[{elapsed:6.2f}s] {msg}")

try:
    log("🌐 Abrindo CarJet...")
    driver.get("https://www.carjet.com/aluguel-carros/index.htm")
    log("✓ Página carregada!")
    
    print("\n" + "="*80)
    print("👉 AGORA É CONTIGO! Faz as seguintes ações:")
    print("="*80)
    
    # Monitorar ações do usuário
    last_url = driver.current_url
    last_title = driver.title
    cookie_popup_seen = False
    second_cookie_seen = False
    form_submitted = False
    
    log(f"URL inicial: {last_url}")
    
    while True:
        time.sleep(0.5)  # Check a cada 0.5s
        
        current_url = driver.current_url
        current_title = driver.title
        
        # Detectar mudança de URL
        if current_url != last_url:
            log(f"🔄 URL mudou: {current_url}")
            last_url = current_url
            
            # Detectar navegação para resultados
            if '/do/list/' in current_url or ('s=' in current_url and 'b=' in current_url):
                log("🎯 CHEGOU À PÁGINA DE RESULTADOS!")
                form_submitted = True
                time.sleep(3)
                log("✅ PROCESSO COMPLETO!")
                break
        
        # Detectar mudança de título
        if current_title != last_title:
            log(f"📄 Título mudou: {current_title}")
            last_title = current_title
        
        # Detectar popups de cookies
        try:
            cookie_info = driver.execute_script("""
                const popups = document.querySelectorAll('[id*=cookie], [class*=cookie], [id*=didomi], [class*=didomi]');
                const visible = [];
                popups.forEach(p => {
                    if (p.offsetParent !== null && p.offsetHeight > 50) {
                        visible.push({
                            id: p.id,
                            classes: p.className,
                            text: p.textContent.substring(0, 100)
                        });
                    }
                });
                return visible;
            """)
            
            if cookie_info and len(cookie_info) > 0:
                if not cookie_popup_seen:
                    log("🍪 1º POPUP DE COOKIE APARECEU!")
                    cookie_popup_seen = True
                    for popup in cookie_info:
                        log(f"   - ID: {popup.get('id')}, Classes: {popup.get('classes')[:50]}")
                elif cookie_popup_seen and not second_cookie_seen:
                    log("🍪🍪 2º POPUP DE COOKIE APARECEU!")
                    second_cookie_seen = True
                    for popup in cookie_info:
                        log(f"   - ID: {popup.get('id')}, Classes: {popup.get('classes')[:50]}")
        except:
            pass
        
        # Detectar preenchimento de campos
        try:
            form_data = driver.execute_script("""
                return {
                    pickup: document.querySelector('input[name="pickup"]')?.value || '',
                    dropoff: document.querySelector('input[name="dropoff"]')?.value || '',
                    fechaRecogida: document.querySelector('input[name="fechaRecogida"]')?.value || '',
                    fechaEntrega: document.querySelector('input[name="fechaEntrega"]')?.value || ''
                };
            """)
            
            # Detectar quando campos são preenchidos
            if form_data['pickup'] and not hasattr(driver, '_pickup_filled'):
                log(f"📝 Campo PICKUP preenchido: {form_data['pickup']}")
                driver._pickup_filled = True
            
            if form_data['fechaRecogida'] and not hasattr(driver, '_data_recogida_filled'):
                log(f"📅 Data RECOLHA preenchida: {form_data['fechaRecogida']}")
                driver._data_recogida_filled = True
            
            if form_data['fechaEntrega'] and not hasattr(driver, '_data_entrega_filled'):
                log(f"📅 Data ENTREGA preenchida: {form_data['fechaEntrega']}")
                driver._data_entrega_filled = True
        except:
            pass
        
        # Timeout após 2 minutos
        if time.time() - t0 > 120:
            log("⏱️ TIMEOUT (2 minutos)")
            break
    
    print("\n" + "="*80)
    print("📊 RESUMO FINAL:")
    print("="*80)
    log(f"URL final: {driver.current_url}")
    log(f"Tempo total: {time.time() - t0:.2f}s")
    print("="*80)
    
    print("\n⏳ Aguardando 10 segundos antes de fechar...")
    time.sleep(10)

except KeyboardInterrupt:
    log("\n⚠️ Interrompido pelo usuário")
except Exception as e:
    log(f"❌ ERRO: {e}")
finally:
    log("🔒 Fechando Chrome...")
    driver.quit()
    log("✓ Concluído!")

print("\n" + "="*80)
print("Agora vou implementar o que observei no código principal!")
print("="*80)
