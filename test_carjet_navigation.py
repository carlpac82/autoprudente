#!/usr/bin/env python3
"""
Teste rápido para verificar se a navegação para /do/list/ funciona
"""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time
from datetime import datetime, timedelta

# Configurar Chrome
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
    
    # Preencher local
    print("📝 Preenchendo local...")
    pickup = driver.find_element(By.ID, 'pickup')
    pickup.clear()
    pickup.send_keys('Albufeira')
    time.sleep(2)
    
    # Clicar no dropdown
    print("📝 Clicando dropdown...")
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
    
    # Preencher datas
    start_date = datetime.now() + timedelta(days=2)
    end_date = start_date + timedelta(days=2)
    
    print(f"📅 Datas: {start_date.strftime('%d/%m/%Y')} - {end_date.strftime('%d/%m/%Y')}")
    
    driver.execute_script(f"""
        document.getElementById('fechaRecogida').value = '{start_date.strftime('%d/%m/%Y')}';
        document.getElementById('fechaDevolucion').value = '{end_date.strftime('%d/%m/%Y')}';
    """)
    
    Select(driver.find_element(By.ID, 'fechaRecogidaSelHour')).select_by_value('15:00')
    Select(driver.find_element(By.ID, 'fechaDevolucionSelHour')).select_by_value('15:00')
    time.sleep(1)
    
    print("🔘 Clicando botão #sendForm...")
    try:
        submit_btn = driver.find_element(By.ID, 'sendForm')
        submit_btn.click()
        print("✅ Botão clicado")
    except Exception as e:
        print(f"⚠️  Erro ao clicar, usando JS: {e}")
        driver.execute_script("document.getElementById('sendForm').click();")
    
    # Aguardar navegação
    print("⏳ Aguardando navegação...")
    time.sleep(5)
    
    # Verificar URL
    current_url = driver.current_url
    print(f"\n🌐 URL atual: {current_url}")
    
    if '/do/list/' in current_url:
        print("✅ SUCESSO! Navegou para /do/list/")
        
        # Aguardar mais um pouco para JS carregar
        time.sleep(8)
        
        # Verificar se tem preços
        html = driver.page_source
        if 'pr-euros' in html:
            print("✅ HTML contém 'pr-euros' - preços presentes!")
            
            # Contar quantos
            count = html.count('pr-euros')
            print(f"📊 Encontrados {count} ocorrências de 'pr-euros'")
        else:
            print("❌ HTML NÃO contém 'pr-euros'")
    else:
        print(f"❌ FALHOU! Não navegou para /do/list/")
        print(f"   URL: {current_url[:100]}")
        
        # Salvar HTML para debug
        with open('test_navigation_failed.html', 'w') as f:
            f.write(driver.page_source)
        print("💾 HTML salvo: test_navigation_failed.html")
    
finally:
    driver.quit()
    print("\n✅ Teste completo!")
