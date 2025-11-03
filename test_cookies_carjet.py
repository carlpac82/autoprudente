#!/usr/bin/env python3
"""Teste específico para aceitar cookies do Carjet"""
import sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

START_URL = "https://www.carjet.com/aluguel-carros/index.htm"

print("=" * 80, flush=True)
print("TESTE DE COOKIES CARJET", flush=True)
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
    
    print("\n⏳ Aguardando 3 segundos...", flush=True)
    time.sleep(3)
    
    print("\n🍪 Procurando banner de cookies...", flush=True)
    
    # Método 1: XPath com texto
    cookie_selectors = [
        ("XPATH", "//button[contains(text(), 'Aceitar todos os cookies')]"),
        ("XPATH", "//button[contains(text(), 'Aceitar todos')]"),
        ("XPATH", "//button[contains(., 'Aceitar todos os cookies')]"),
        ("CSS", "button[class*='cookie']"),
        ("CSS", "button[class*='accept']"),
    ]
    
    cookie_found = False
    for method, selector in cookie_selectors:
        try:
            print(f"   Tentando: {method} = {selector}", flush=True)
            if method == "XPATH":
                cookie_btn = driver.find_element(By.XPATH, selector)
            else:
                cookie_btn = driver.find_element(By.CSS_SELECTOR, selector)
            
            if cookie_btn and cookie_btn.is_displayed():
                print(f"   ✅ Botão encontrado e visível!", flush=True)
                print(f"   Texto do botão: {cookie_btn.text}", flush=True)
                cookie_btn.click()
                print("   ✅ CLICADO!", flush=True)
                cookie_found = True
                time.sleep(2)
                break
            else:
                print(f"   ⚠️  Botão encontrado mas não visível", flush=True)
        except Exception as e:
            print(f"   ❌ Não encontrado: {e}", flush=True)
    
    if not cookie_found:
        print("\n❌ Nenhum botão de cookies encontrado!", flush=True)
        print("📝 Vou tentar listar todos os botões da página...", flush=True)
        try:
            all_buttons = driver.find_elements(By.TAG_NAME, "button")
            print(f"   Total de botões na página: {len(all_buttons)}", flush=True)
            for i, btn in enumerate(all_buttons[:10], 1):
                try:
                    print(f"   Botão {i}: '{btn.text}' (visível: {btn.is_displayed()})", flush=True)
                except:
                    print(f"   Botão {i}: [erro ao ler]", flush=True)
        except Exception as e:
            print(f"   Erro ao listar botões: {e}", flush=True)
    else:
        print("\n✅ Cookies aceites com sucesso!", flush=True)
    
    print("\n" + "=" * 80, flush=True)
    print("Chrome ficará aberto por 60 segundos", flush=True)
    print("=" * 80, flush=True)
    
    for i in range(60, 0, -10):
        print(f"⏱️  {i} segundos...", flush=True)
        time.sleep(10)
    
except Exception as e:
    print(f"\n❌ ERRO: {e}", flush=True)
    import traceback
    traceback.print_exc()
    time.sleep(30)
finally:
    driver.quit()
    print("\n👋 Chrome fechado", flush=True)
