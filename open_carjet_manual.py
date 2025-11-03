#!/usr/bin/env python3
"""Abre Carjet para teste manual - você preenche o formulário"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

# Escolha a versão:
# PT: https://www.carjet.com/aluguel-carros/index.htm
# EN: https://www.carjet.com/index.htm
START_URL = "https://www.carjet.com/aluguel-carros/index.htm"

print("=" * 80)
print("CARJET - TESTE MANUAL")
print("=" * 80)
print(f"URL: {START_URL}")
print("\n📝 INSTRUÇÕES:")
print("   1. Chrome vai abrir")
print("   2. Preencha manualmente:")
print("      - Recolha: Albufeira Cidade")
print("      - Devolução: Faro Aeroporto (FAO)")
print("      - Datas: 10-15 Nov 2025")
print("   3. Clique em Pesquisar")
print("   4. Filtre por AUTOPRUDENTE")
print("   5. Janela fica aberta 5 MINUTOS para você testar")
print("=" * 80)

chrome_options = Options()
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")

print("\n🚀 Abrindo Chrome...")
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

try:
    driver.get(START_URL)
    print(f"✅ Página aberta: {START_URL}")
    
    # Aceitar cookies automaticamente - MÉTODO CORRETO
    time.sleep(3)
    try:
        # Procurar pelo texto dos botões de cookies em português
        cookie_selectors = [
            "//button[contains(text(), 'Aceitar todos os cookies')]",
            "//button[contains(text(), 'Aceitar todos')]",
            "//button[contains(., 'Aceitar todos os cookies')]",
        ]
        
        cookie_accepted = False
        for sel in cookie_selectors:
            try:
                cookie_btn = driver.find_element(By.XPATH, sel)
                if cookie_btn and cookie_btn.is_displayed():
                    cookie_btn.click()
                    print("✅ Cookies aceites automaticamente")
                    cookie_accepted = True
                    time.sleep(2)
                    break
            except:
                pass
        
        if not cookie_accepted:
            print("⚠️  Banner de cookies não encontrado")
    except Exception as e:
        print(f"⚠️  Erro ao aceitar cookies: {e}")
    
    print("\n" + "=" * 80)
    print("✅ CHROME ABERTO - PREENCHA O FORMULÁRIO MANUALMENTE")
    print("   Janela ficará aberta por 5 MINUTOS (300 segundos)")
    print("=" * 80)
    
    # Aguardar 5 minutos
    for i in range(300, 0, -30):
        print(f"⏱️  Fechando em {i} segundos...")
        time.sleep(30)
    
except KeyboardInterrupt:
    print("\n⚠️  Interrompido pelo usuário")
except Exception as e:
    print(f"\n❌ ERRO: {e}")
    import traceback
    traceback.print_exc()
finally:
    driver.quit()
    print("\n👋 Chrome fechado")
