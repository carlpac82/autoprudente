#!/usr/bin/env python3
"""
Teste usando form.submit() diretamente
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

print("🚀 Iniciando teste com form.submit()...")
driver = webdriver.Chrome(options=chrome_options)

try:
    driver.get('https://www.carjet.com/aluguel-carros/index.htm')
    time.sleep(2)
    
    # Rejeitar cookies
    try:
        driver.find_element(By.XPATH, "//button[contains(text(), 'Rejeitar')]").click()
        print("✅ Cookies rejeitados")
        time.sleep(1)
    except:
        pass
    
    # Preencher formulário
    print("📝 Preenchendo formulário...")
    pickup = driver.find_element(By.ID, 'pickup')
    pickup.clear()
    pickup.send_keys('Albufeira')
    time.sleep(2)
    
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
    
    start_date = datetime.now() + timedelta(days=2)
    end_date = start_date + timedelta(days=2)
    
    driver.execute_script(f"""
        document.getElementById('fechaRecogida').value = '{start_date.strftime('%d/%m/%Y')}';
        document.getElementById('fechaDevolucion').value = '{end_date.strftime('%d/%m/%Y')}';
    """)
    
    Select(driver.find_element(By.ID, 'fechaRecogidaSelHour')).select_by_value('15:00')
    Select(driver.find_element(By.ID, 'fechaDevolucionSelHour')).select_by_value('15:00')
    time.sleep(1)
    
    # Submit usando form.submit() - SEMPRE funciona
    print("🔘 Submetendo com form.submit()...")
    driver.execute_script("""
        const form = document.querySelector('form');
        if (form) {
            form.submit();
        }
    """)
    print("✅ Submit executado")
    
    # Aguardar navegação
    print("\n⏳ Aguardando navegação...")
    time.sleep(5)
    
    max_wait = 30
    waited = 0
    success = False
    
    while waited < max_wait:
        current_url = driver.current_url
        if '/do/list/' in current_url:
            print(f"✅ Navegou para /do/list/ após {waited}s")
            success = True
            break
        else:
            print(f"   {waited}s - Aguardando... {current_url[:60]}...")
            time.sleep(3)
            waited += 3
    
    if success:
        print("\n✅ SUCESSO! Na página de resultados")
        print(f"🌐 URL: {driver.current_url[:100]}")
        
        # Aguardar JS
        print("\n⏳ Aguardando JavaScript...")
        time.sleep(8)
        
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        
        articles = soup.select('section.newcarlist article')
        print(f"\n📊 Articles: {len(articles)}")
        
        if articles:
            first = articles[0]
            h2 = first.find('h2')
            if h2:
                print(f"🚗 Primeiro carro: {h2.get_text(strip=True)}")
            
            prices = first.select('.price.pr-euros')
            print(f"💰 Preços .pr-euros: {len(prices)}")
            
            if prices:
                for i, p in enumerate(prices[:2]):
                    print(f"   [{i}] {p.get_text(strip=True)}")
                print("\n✅✅✅ PREÇOS ENCONTRADOS! Sistema está funcionando!")
            else:
                print("❌ Sem preços .pr-euros")
        
        with open('test_form_submit_success.html', 'w') as f:
            f.write(html)
        print("\n💾 HTML: test_form_submit_success.html")
    else:
        print(f"\n❌ FALHOU - Timeout após {waited}s")
        print(f"URL final: {driver.current_url}")
        
finally:
    driver.quit()
