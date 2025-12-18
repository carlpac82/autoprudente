#!/usr/bin/env python3
"""
Teste completo do fluxo de scraping com as correções
"""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import time
from datetime import datetime, timedelta

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15')

print("🚀 Iniciando Chrome...")
driver = webdriver.Chrome(options=chrome_options)

try:
    print("📱 Acessando CarJet...")
    driver.get('https://www.carjet.com/aluguel-carros/index.htm')
    time.sleep(2)
    
    # Rejeitar cookies
    try:
        driver.find_element(By.XPATH, "//button[contains(text(), 'Rejeitar')]").click()
        print("✅ Cookies rejeitados")
        time.sleep(1)
    except:
        print("⚠️  Sem popup de cookies")
    
    # PASSO 1: Local
    print("\n📝 PASSO 1: Preenchendo local...")
    pickup = driver.find_element(By.ID, 'pickup')
    pickup.clear()
    pickup.send_keys('Albufeira')
    time.sleep(2)
    
    # PASSO 2: Dropdown
    print("📝 PASSO 2: Clicando dropdown...")
    driver.execute_script("""
        const items = document.querySelectorAll('#recogida_lista li');
        for (let item of items) {
            if (item.offsetParent !== null) {
                item.click();
                break;
            }
        }
    """)
    time.sleep(1)
    
    # PASSO 3: Datas
    start_date = datetime.now() + timedelta(days=2)
    end_date = start_date + timedelta(days=2)
    
    print(f"📅 PASSO 3: Datas: {start_date.strftime('%d/%m/%Y')} - {end_date.strftime('%d/%m/%Y')}")
    
    driver.execute_script(f"""
        document.getElementById('fechaRecogida').value = '{start_date.strftime('%d/%m/%Y')}';
        document.getElementById('fechaDevolucion').value = '{end_date.strftime('%d/%m/%Y')}';
    """)
    
    Select(driver.find_element(By.ID, 'fechaRecogidaSelHour')).select_by_value('15:00')
    Select(driver.find_element(By.ID, 'fechaDevolucionSelHour')).select_by_value('15:00')
    time.sleep(1)
    
    # PASSO 4: Submit via JS
    print("🔘 PASSO 4: Submetendo via JavaScript...")
    driver.execute_script("document.getElementById('sendForm').click();")
    print("✅ Clique executado")
    
    # Aguardar navegação
    print("\n⏳ Aguardando navegação...")
    time.sleep(5)
    
    # Loop aguardando /do/list/
    max_wait = 30
    waited = 0
    while waited < max_wait:
        current_url = driver.current_url
        if '/do/list/' in current_url:
            print(f"✅ Navegou para /do/list/ após {waited}s")
            break
        else:
            print(f"   {waited}s - URL: {current_url[:60]}...")
            time.sleep(3)
            waited += 3
    
    final_url = driver.current_url
    print(f"\n🌐 URL final: {final_url[:100]}")
    
    if '/do/list/' in final_url:
        print("✅ SUCESSO - Na página de resultados!")
        
        # Aguardar JavaScript carregar preços
        print("\n⏳ Aguardando JavaScript carregar preços...")
        time.sleep(8)
        
        # Analisar HTML
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        
        # Verificar articles
        articles = soup.select('section.newcarlist article')
        print(f"\n📊 Articles encontrados: {len(articles)}")
        
        if articles:
            print("\n🔍 Analisando primeiro article:")
            first = articles[0]
            
            # Nome do carro
            h2 = first.find('h2')
            if h2:
                print(f"   🚗 Carro: {h2.get_text(strip=True)}")
            
            # Preços
            price_spans = first.select('.price.pr-euros')
            print(f"   💰 Spans .price.pr-euros: {len(price_spans)}")
            
            if price_spans:
                for i, span in enumerate(price_spans[:3]):
                    print(f"      [{i}] {span.get('class')} = '{span.get_text(strip=True)}'")
                print("\n✅ PREÇOS ENCONTRADOS!")
            else:
                print("   ❌ Nenhum .price.pr-euros encontrado")
                
                # Verificar todos os spans com 'price'
                all_price_spans = first.find_all('span', class_=lambda x: x and 'price' in str(x))
                print(f"   📊 Spans com 'price' na classe: {len(all_price_spans)}")
                for i, sp in enumerate(all_price_spans[:5]):
                    print(f"      [{i}] {sp.get('class')} = '{sp.get_text(strip=True)[:50]}'")
        
        # Salvar HTML
        with open('test_scraping_success.html', 'w') as f:
            f.write(html)
        print("\n💾 HTML salvo: test_scraping_success.html")
        
    else:
        print(f"❌ FALHOU - Não navegou para /do/list/")
        print(f"   URL: {final_url[:150]}")
        
        with open('test_scraping_failed.html', 'w') as f:
            f.write(driver.page_source)
        print("💾 HTML salvo: test_scraping_failed.html")
    
finally:
    driver.quit()
    print("\n✅ Teste completo!")
