#!/usr/bin/env python3
"""Script de teste visual - Chrome fica aberto 60 segundos"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

TEST_URL = "https://www.carjet.com/pt/aluguer-de-carros/portugal/faro/albufeira/?fecRec=2025-11-10&fecDev=2025-11-15&horRec=10:00&horDev=10:00&lugRec=Albufeira&lugDev=Albufeira&codLugRec=&codLugDev=&edad=30"

print("=" * 80)
print("TESTE VISUAL - CHROME FICARÁ ABERTO 60 SEGUNDOS")
print("=" * 80)

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
    except Exception as e:
        print(f"⚠️  Sem banner de cookies: {e}")
    
    # Verificar página atual
    print(f"\n📄 URL atual: {driver.current_url}")
    print(f"📄 Título: {driver.title}")
    
    # Procurar checkbox AUTOPRUDENTE
    print("\n🔍 Procurando checkbox AUTOPRUDENTE (#chkAUP)...")
    try:
        aup_checkbox = driver.find_element(By.ID, "chkAUP")
        print(f"✅ Encontrado! Visível: {aup_checkbox.is_displayed()}, Marcado: {aup_checkbox.is_selected()}")
        
        # Desmarcar todos
        print("\n📋 Desmarcando todos os suppliers...")
        driver.execute_script("""
            const checked = document.querySelectorAll('input[name="frmPrv"]:checked');
            console.log('Desmarcando', checked.length, 'checkboxes');
            checked.forEach(cb => cb.click());
        """)
        time.sleep(2)
        
        # Marcar AUTOPRUDENTE
        print("✅ Marcando AUTOPRUDENTE...")
        driver.execute_script("""
            const aup = document.querySelector('#chkAUP');
            if (aup) {
                console.log('Clicando em AUTOPRUDENTE');
                aup.click();
            }
        """)
        time.sleep(5)
        print("✅ Filtro aplicado, aguardando resultados...")
        
    except Exception as e:
        print(f"❌ Erro ao manipular checkbox: {e}")
    
    # Procurar resultados com diferentes seletores
    print("\n🚗 Procurando resultados com diferentes seletores...")
    
    selectors = [
        "section.newcarlist article",
        "article.car",
        ".car-item",
        "li.result",
        "[class*='car']",
    ]
    
    for selector in selectors:
        try:
            elements = driver.find_elements(By.CSS_SELECTOR, selector)
            print(f"   {selector}: {len(elements)} elementos")
        except:
            print(f"   {selector}: erro")
    
    # Tentar extrair HTML da página
    print("\n📝 Verificando estrutura HTML...")
    try:
        body_html = driver.find_element(By.TAG_NAME, "body").get_attribute("innerHTML")
        if "newcarlist" in body_html:
            print("✅ Encontrado 'newcarlist' no HTML")
        else:
            print("❌ 'newcarlist' NÃO encontrado no HTML")
            
        if "article" in body_html:
            print("✅ Encontrado 'article' no HTML")
        else:
            print("❌ 'article' NÃO encontrado no HTML")
    except Exception as e:
        print(f"❌ Erro ao verificar HTML: {e}")
    
    # Scroll para carregar lazy loading
    print("\n📜 Fazendo scroll...")
    for i in range(3):
        driver.execute_script("window.scrollBy(0, 1000);")
        time.sleep(1)
    
    # Verificar novamente
    print("\n🔄 Verificando resultados após scroll...")
    articles = driver.find_elements(By.CSS_SELECTOR, "section.newcarlist article")
    print(f"✅ Encontrados {len(articles)} artigos")
    
    if len(articles) > 0:
        print("\n📊 Primeiros 3 resultados:")
        for i, art in enumerate(articles[:3], 1):
            try:
                car = art.find_element(By.CSS_SELECTOR, "h2").text
                price = art.find_element(By.CSS_SELECTOR, ".pr-euros").text
                print(f"  {i}. {car} - {price}")
            except Exception as e:
                print(f"  {i}. [Erro: {e}]")
    
    print("\n" + "=" * 80)
    print("✅ CHROME FICARÁ ABERTO POR 60 SEGUNDOS")
    print("   Inspecione a página manualmente!")
    print("=" * 80)
    
    # Aguardar 60 segundos
    for i in range(60, 0, -10):
        print(f"⏱️  Fechando em {i} segundos...")
        time.sleep(10)
    
except Exception as e:
    print(f"\n❌ ERRO: {e}")
    import traceback
    traceback.print_exc()
    time.sleep(30)
finally:
    driver.quit()
    print("\n👋 Chrome fechado")
