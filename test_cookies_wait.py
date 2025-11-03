#!/usr/bin/env python3
"""Teste com espera explícita para o banner de cookies"""
import sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

START_URL = "https://www.carjet.com/aluguel-carros/index.htm"

print("=" * 80, flush=True)
print("TESTE COM ESPERA EXPLÍCITA - CARJET COOKIES", flush=True)
print("=" * 80, flush=True)

chrome_options = Options()
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")

print("\n🚀 Iniciando Chrome...", flush=True)
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

try:
    print(f"📍 Navegando para: {START_URL}", flush=True)
    driver.get(START_URL)
    print("✅ Página carregada", flush=True)
    
    print("\n⏳ Aguardando banner de cookies aparecer (até 15 segundos)...", flush=True)
    
    cookie_found = False
    
    # Estratégia 1: Aguardar elemento com WebDriverWait
    try:
        print("   Estratégia 1: WebDriverWait com XPATH...", flush=True)
        cookie_btn = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Aceitar todos os cookies')]"))
        )
        print(f"   ✅ Botão encontrado: '{cookie_btn.text}'", flush=True)
        cookie_btn.click()
        print("   ✅ CLICADO!", flush=True)
        cookie_found = True
        time.sleep(2)
    except Exception as e:
        print(f"   ❌ Estratégia 1 falhou: {type(e).__name__}", flush=True)
    
    # Estratégia 2: Procurar por texto parcial
    if not cookie_found:
        try:
            print("   Estratégia 2: Texto parcial 'Aceitar todos'...", flush=True)
            cookie_btn = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Aceitar todos')]"))
            )
            print(f"   ✅ Botão encontrado: '{cookie_btn.text}'", flush=True)
            cookie_btn.click()
            print("   ✅ CLICADO!", flush=True)
            cookie_found = True
            time.sleep(2)
        except Exception as e:
            print(f"   ❌ Estratégia 2 falhou: {type(e).__name__}", flush=True)
    
    # Estratégia 3: JavaScript para procurar e clicar
    if not cookie_found:
        try:
            print("   Estratégia 3: JavaScript direto...", flush=True)
            time.sleep(3)
            result = driver.execute_script("""
                // Procurar todos os botões
                const buttons = Array.from(document.querySelectorAll('button'));
                console.log('Total de botões:', buttons.length);
                
                // Procurar botão com texto "Aceitar todos os cookies"
                const cookieBtn = buttons.find(btn => 
                    btn.textContent.includes('Aceitar todos os cookies') ||
                    btn.textContent.includes('Aceitar todos')
                );
                
                if (cookieBtn) {
                    console.log('Botão encontrado:', cookieBtn.textContent);
                    cookieBtn.click();
                    return 'CLICADO: ' + cookieBtn.textContent;
                }
                
                return 'NÃO ENCONTRADO';
            """)
            print(f"   Resultado JavaScript: {result}", flush=True)
            if "CLICADO" in result:
                cookie_found = True
                time.sleep(2)
        except Exception as e:
            print(f"   ❌ Estratégia 3 falhou: {e}", flush=True)
    
    # Estratégia 4: Listar TODOS os botões e procurar manualmente
    if not cookie_found:
        try:
            print("   Estratégia 4: Listar todos os botões...", flush=True)
            time.sleep(2)
            all_buttons = driver.find_elements(By.TAG_NAME, "button")
            print(f"   Total de botões: {len(all_buttons)}", flush=True)
            
            for i, btn in enumerate(all_buttons, 1):
                try:
                    btn_text = btn.text.strip()
                    if btn_text:
                        print(f"   Botão {i}: '{btn_text}' (visível: {btn.is_displayed()})", flush=True)
                        if "Aceitar" in btn_text and "cookies" in btn_text:
                            print(f"   ✅ ENCONTRADO! Clicando...", flush=True)
                            btn.click()
                            cookie_found = True
                            time.sleep(2)
                            break
                except:
                    pass
        except Exception as e:
            print(f"   ❌ Estratégia 4 falhou: {e}", flush=True)
    
    if cookie_found:
        print("\n✅ SUCESSO! Cookies aceites!", flush=True)
    else:
        print("\n❌ FALHA! Não foi possível aceitar cookies", flush=True)
        # Screenshot para debug
        try:
            screenshot_path = "/Users/filipepacheco/CascadeProjects/RentalPriceTrackerPerDay/debug_cookies_wait.png"
            driver.save_screenshot(screenshot_path)
            print(f"📸 Screenshot salvo: {screenshot_path}", flush=True)
        except:
            pass
    
    print("\n" + "=" * 80, flush=True)
    print("Chrome ficará aberto por 90 segundos", flush=True)
    print("=" * 80, flush=True)
    
    for i in range(90, 0, -15):
        print(f"⏱️  {i} segundos...", flush=True)
        time.sleep(15)
    
except Exception as e:
    print(f"\n❌ ERRO GERAL: {e}", flush=True)
    import traceback
    traceback.print_exc()
    time.sleep(30)
finally:
    driver.quit()
    print("\n👋 Chrome fechado", flush=True)
