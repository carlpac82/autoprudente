#!/usr/bin/env python3
"""Script de teste com a página correta do Carjet"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import time

# Página inicial CORRETA - Português
START_URL = "https://www.carjet.com/aluguel-carros/index.htm"

print("=" * 80)
print("TESTE COM PÁGINA CORRETA DO CARJET")
print("=" * 80)
print(f"URL Inicial: {START_URL}")
print("Locais: Albufeira Cidade → Faro Aeroporto (FAO)")
print("=" * 80)

chrome_options = Options()
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)

print("\n🚀 Iniciando Chrome...")
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

try:
    # Ir para página inicial
    print(f"\n📍 Navegando para: {START_URL}")
    driver.get(START_URL)
    time.sleep(3)
    
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
    
    print(f"\n📄 URL atual: {driver.current_url}")
    print(f"📄 Título: {driver.title}")
    
    # Procurar formulário de pesquisa
    print("\n🔍 Procurando formulário de pesquisa...")
    
    # Tentar preencher local de recolha (Albufeira Cidade)
    print("\n📍 Preenchendo local de recolha: Albufeira Cidade")
    try:
        # Procurar campo de input para local de recolha
        pickup_input = driver.find_element(By.ID, "lugRec")
        pickup_input.clear()
        pickup_input.send_keys("Albufeira")
        time.sleep(2)
        
        # Aguardar dropdown aparecer e selecionar "Albufeira Cidade"
        print("   Aguardando dropdown...")
        time.sleep(2)
        pickup_input.send_keys(Keys.ARROW_DOWN)
        time.sleep(1)
        pickup_input.send_keys(Keys.ENTER)
        print("✅ Local de recolha selecionado")
        time.sleep(1)
        
    except Exception as e:
        print(f"❌ Erro ao preencher local de recolha: {e}")
    
    # Tentar preencher local de devolução (Faro Aeroporto)
    print("\n📍 Preenchendo local de devolução: Faro Aeroporto (FAO)")
    try:
        # Verificar se há checkbox "devolver em local diferente"
        try:
            diff_location = driver.find_element(By.ID, "chkLugDif")
            if not diff_location.is_selected():
                diff_location.click()
                print("✅ Checkbox 'local diferente' marcado")
                time.sleep(1)
        except:
            pass
        
        dropoff_input = driver.find_element(By.ID, "lugDev")
        dropoff_input.clear()
        dropoff_input.send_keys("Faro")
        time.sleep(2)
        
        # Aguardar dropdown e selecionar aeroporto
        print("   Aguardando dropdown...")
        time.sleep(2)
        dropoff_input.send_keys(Keys.ARROW_DOWN)
        time.sleep(1)
        dropoff_input.send_keys(Keys.ENTER)
        print("✅ Local de devolução selecionado")
        time.sleep(1)
        
    except Exception as e:
        print(f"❌ Erro ao preencher local de devolução: {e}")
    
    # Preencher datas (exemplo: 10-15 Nov 2025)
    print("\n📅 Preenchendo datas...")
    try:
        # Data recolha
        date_pickup = driver.find_element(By.ID, "fecRec")
        date_pickup.clear()
        date_pickup.send_keys("10/11/2025")
        
        # Data devolução
        date_dropoff = driver.find_element(By.ID, "fecDev")
        date_dropoff.clear()
        date_dropoff.send_keys("15/11/2025")
        
        print("✅ Datas preenchidas")
        time.sleep(1)
        
    except Exception as e:
        print(f"⚠️  Erro ao preencher datas: {e}")
    
    # Clicar no botão de pesquisa
    print("\n🔍 Clicando no botão de pesquisa...")
    try:
        search_btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit'], input[type='submit'], .btn-search")
        search_btn.click()
        print("✅ Botão clicado")
        
        # Aguardar resultados carregarem
        print("\n⏳ Aguardando resultados carregarem...")
        time.sleep(8)
        
    except Exception as e:
        print(f"❌ Erro ao clicar no botão: {e}")
    
    print(f"\n📄 URL após pesquisa: {driver.current_url}")
    
    # Procurar checkbox AUTOPRUDENTE nos resultados
    print("\n🔍 Procurando checkbox AUTOPRUDENTE nos resultados...")
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
        print("✅ Filtro AUTOPRUDENTE aplicado")
        
    except Exception as e:
        print(f"❌ Erro ao manipular checkbox AUTOPRUDENTE: {e}")
    
    # Procurar resultados
    print("\n🚗 Procurando resultados...")
    time.sleep(3)
    
    selectors = [
        "section.newcarlist article",
        "article.car",
        ".car-item",
        "li.result",
    ]
    
    for selector in selectors:
        try:
            elements = driver.find_elements(By.CSS_SELECTOR, selector)
            print(f"   {selector}: {len(elements)} elementos")
            if len(elements) > 0:
                print(f"   ✅ Encontrados resultados com: {selector}")
                break
        except:
            print(f"   {selector}: erro")
    
    # Tentar extrair primeiros resultados
    articles = driver.find_elements(By.CSS_SELECTOR, "section.newcarlist article")
    print(f"\n✅ Total de artigos encontrados: {len(articles)}")
    
    if len(articles) > 0:
        print("\n📊 Primeiros 3 resultados:")
        for i, art in enumerate(articles[:3], 1):
            try:
                car = art.find_element(By.CSS_SELECTOR, "h2").text
                price = art.find_element(By.CSS_SELECTOR, ".pr-euros").text
                supplier = ""
                try:
                    supplier_img = art.find_element(By.CSS_SELECTOR, "img[src*='/prv/']")
                    supplier = supplier_img.get_attribute("alt")
                except:
                    pass
                print(f"  {i}. {car} - {price} - {supplier}")
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
    print(f"\n❌ ERRO GERAL: {e}")
    import traceback
    traceback.print_exc()
    time.sleep(30)
finally:
    driver.quit()
    print("\n👋 Chrome fechado")
