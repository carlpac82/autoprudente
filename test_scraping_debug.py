#!/usr/bin/env python3
"""Script de teste visual para debugging do scraping"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

# URL de teste
TEST_URL = "https://www.carjet.com/pt/aluguer-de-carros/portugal/faro/albufeira/?fecRec=2025-11-10&fecDev=2025-11-15&horRec=10:00&horDev=10:00&lugRec=Albufeira&lugDev=Albufeira&codLugRec=&codLugDev=&edad=30"

print("=" * 80)
print("TESTE VISUAL DE SCRAPING CARJET")
print("=" * 80)

# Chrome em modo VISÍVEL
chrome_options = Options()
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")

print("\n🚀 Iniciando Chrome...")
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

try:
    print(f"📍 Navegando para Carjet...")
    driver.get(TEST_URL)
    
    print("⏳ Aguardando 5 segundos...")
    time.sleep(5)
    
    # Aceitar cookies
    print("\n🍪 Tentando aceitar cookies...")
    try:
        cookie_btn = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.ID, "didomi-notice-agree-button"))
        )
        cookie_btn.click()
        print("✅ Cookies aceites")
        time.sleep(2)
    except:
        print("⚠️  Sem banner de cookies")
    
    # Procurar checkbox AUTOPRUDENTE
    print("\n🔍 Procurando checkbox AUTOPRUDENTE...")
    try:
        aup_checkbox = driver.find_element(By.ID, "chkAUP")
        print(f"✅ Encontrado! Visível: {aup_checkbox.is_displayed()}, Marcado: {aup_checkbox.is_selected()}")
        
        # Desmarcar todos
        print("\n📋 Desmarcando todos os suppliers...")
        driver.execute_script("""
            document.querySelectorAll('input[name="frmPrv"]:checked').forEach(cb => cb.click());
        """)
        time.sleep(2)
        
        # Marcar AUTOPRUDENTE
        print("✅ Marcando AUTOPRUDENTE...")
        driver.execute_script("document.querySelector('#chkAUP').click();")
        time.sleep(3)
        
    except Exception as e:
        print(f"❌ Erro: {e}")
    
    # Procurar resultados
    print("\n🚗 Procurando resultados...")
    time.sleep(3)
    articles = driver.find_elements(By.CSS_SELECTOR, "section.newcarlist article")
    print(f"✅ Encontrados {len(articles)} artigos")
    
    if len(articles) > 0:
        print("\n📊 Primeiros 3 resultados:")
        for i, art in enumerate(articles[:3], 1):
            try:
                car = art.find_element(By.CSS_SELECTOR, "h2").text
                price = art.find_element(By.CSS_SELECTOR, ".pr-euros").text
                print(f"  {i}. {car} - {price}")
            except:
                print(f"  {i}. [Erro ao extrair dados]")
    
    print("\n✅ Teste concluído! Janela do Chrome ficará aberta.")
    print("   Pressione Ctrl+C para fechar quando terminar de inspecionar.")
    
    # Manter janela aberta
    input("\nPressione ENTER para fechar o Chrome...")
    
except Exception as e:
    print(f"\n❌ ERRO: {e}")
    input("\nPressione ENTER para fechar...")
finally:
    driver.quit()
    print("\n👋 Chrome fechado")
