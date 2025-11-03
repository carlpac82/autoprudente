#!/usr/bin/env python3
"""Teste para encontrar cookies dentro de iframes"""
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
print("TESTE DE COOKIES EM IFRAME - CARJET", flush=True)
print("=" * 80, flush=True)

chrome_options = Options()
chrome_options.add_argument("--start-maximized")

print("\n🚀 Iniciando Chrome...", flush=True)
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

try:
    print(f"📍 Navegando para: {START_URL}", flush=True)
    driver.get(START_URL)
    print("✅ Página carregada", flush=True)
    
    print("\n⏳ Aguardando 5 segundos para banner aparecer...", flush=True)
    time.sleep(5)
    
    # Procurar iframes
    print("\n🔍 Procurando iframes na página...", flush=True)
    iframes = driver.find_elements(By.TAG_NAME, "iframe")
    print(f"   Total de iframes encontrados: {len(iframes)}", flush=True)
    
    for i, iframe in enumerate(iframes, 1):
        try:
            iframe_id = iframe.get_attribute("id") or "[sem id]"
            iframe_src = iframe.get_attribute("src") or "[sem src]"
            print(f"   Iframe {i}: id='{iframe_id}', src='{iframe_src[:80]}'", flush=True)
        except:
            print(f"   Iframe {i}: [erro ao ler atributos]", flush=True)
    
    # Tentar encontrar botão no contexto principal primeiro
    print("\n🍪 Tentando encontrar botão no contexto principal...", flush=True)
    cookie_found = False
    
    try:
        # Aguardar botão aparecer
        cookie_btn = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Aceitar')]"))
        )
        if cookie_btn.is_displayed():
            print(f"   ✅ Botão encontrado: '{cookie_btn.text}'", flush=True)
            cookie_btn.click()
            print("   ✅ CLICADO!", flush=True)
            cookie_found = True
            time.sleep(2)
    except Exception as e:
        print(f"   ❌ Não encontrado no contexto principal: {e}", flush=True)
    
    # Se não encontrou, tentar em cada iframe
    if not cookie_found and len(iframes) > 0:
        print("\n🔍 Procurando dentro dos iframes...", flush=True)
        for i, iframe in enumerate(iframes, 1):
            try:
                print(f"   Mudando para iframe {i}...", flush=True)
                driver.switch_to.frame(iframe)
                
                # Procurar botão dentro do iframe
                try:
                    cookie_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Aceitar')]")
                    if cookie_btn.is_displayed():
                        print(f"   ✅ Botão encontrado no iframe {i}: '{cookie_btn.text}'", flush=True)
                        cookie_btn.click()
                        print("   ✅ CLICADO!", flush=True)
                        cookie_found = True
                        driver.switch_to.default_content()
                        time.sleep(2)
                        break
                except:
                    print(f"   ❌ Não encontrado no iframe {i}", flush=True)
                
                # Voltar ao contexto principal
                driver.switch_to.default_content()
            except Exception as e:
                print(f"   ❌ Erro ao processar iframe {i}: {e}", flush=True)
                driver.switch_to.default_content()
    
    if not cookie_found:
        print("\n❌ Botão de cookies NÃO encontrado em nenhum lugar!", flush=True)
        
        # Tentar screenshot para debug
        try:
            screenshot_path = "/Users/filipepacheco/CascadeProjects/RentalPriceTrackerPerDay/debug_cookies.png"
            driver.save_screenshot(screenshot_path)
            print(f"📸 Screenshot salvo em: {screenshot_path}", flush=True)
        except:
            pass
    else:
        print("\n✅ Cookies aceites com sucesso!", flush=True)
    
    print("\n" + "=" * 80, flush=True)
    print("Chrome ficará aberto por 90 segundos para você inspecionar", flush=True)
    print("=" * 80, flush=True)
    
    for i in range(90, 0, -15):
        print(f"⏱️  {i} segundos...", flush=True)
        time.sleep(15)
    
except Exception as e:
    print(f"\n❌ ERRO: {e}", flush=True)
    import traceback
    traceback.print_exc()
    time.sleep(30)
finally:
    driver.quit()
    print("\n👋 Chrome fechado", flush=True)
